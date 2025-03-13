import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional

from config.llm_configs import get_llm_configs, get_available_llms
from core.browser import BrowserAutomation
from core.evaluator import ResponseEvaluator
from utils.storage import store_result

logger = logging.getLogger(__name__)


class LLMResponseAggregator:
    def __init__(self, selected_llms=None, headless=True):
        """
        Initialize the LLM Response Aggregator.

        Args:
            selected_llms: List of LLM names to use. If None, use all available LLMs.
            headless: Whether to run browsers in headless mode.
        """

        available_llms = get_available_llms()
        if selected_llms:
            self.llm_names = [llm for llm in selected_llms if llm in available_llms]
            if not self.llm_names:
                logger.warning(
                    f"None of the selected LLMs {selected_llms} are available. Using all available LLMs."
                )
                self.llm_names = available_llms
        else:
            self.llm_names = available_llms

        logger.info(f"Using LLMs: {self.llm_names}")

        self.browser = BrowserAutomation(headless=headless)
        self.evaluator = ResponseEvaluator()

    async def process_query(self, user_query: str) -> Dict:
        """Process a user query through multiple LLMs and return the best response."""
        responses = await self._get_all_responses(user_query)
        if not responses:
            return {"error": "Failed to get responses from any LLM"}

        ranked_responses = self.evaluator.evaluate_and_rank_responses(
            user_query, responses
        )
        best_response = ranked_responses[0]

        result = {
            "original_query": user_query,
            "best_response": {
                "source": best_response[0],
                "content": best_response[1],
                "score": best_response[2],
                "timestamp": best_response[3],
            },
            "all_responses": [
                {
                    "source": source,
                    "content": content,
                    "score": score,
                    "timestamp": timestamp,
                }
                for source, content, score, timestamp in ranked_responses
            ],
        }

        filename = store_result(result)
        result["filename"] = filename

        return result

    async def _get_all_responses(self, query: str) -> List[Tuple[str, str, datetime]]:
        """Get responses from all configured LLMs asynchronously."""
        tasks = []
        for llm_name in self.llm_names:
            config = get_llm_configs(llm_name)
            if not config:
                logger.warning(f"No configuration found for LLM: {llm_name}")
                continue

            tasks.append(self._get_llm_response(llm_name, config, query))

        responses = await asyncio.gather(*tasks)
        return [resp for resp in responses if resp is not None]

    async def _get_llm_response(
        self, llm_name: str, config: Dict, query: str
    ) -> Optional[Tuple[str, str, datetime]]:
        """Get response from a specific LLM."""
        try:
            return await self.browser.get_response(llm_name, config, query)
        except Exception as e:
            logger.exception(f"Error getting response from {llm_name}: {str(e)}")
            return None
