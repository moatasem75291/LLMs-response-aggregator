import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional, Tuple
import time
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.common.exceptions import TimeoutException


logger = logging.getLogger(__name__)


class LLMBrowserAutomation(ABC):
    """Abstract base class for LLM browser automation implementations."""

    def __init__(self, headless: bool = True):
        self.headless = headless

    def get_chrome_options(self):
        """Get Chrome options for browser."""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    @abstractmethod
    def setup_driver(self, config: Dict):
        """Set up and configure the browser driver."""
        pass

    @abstractmethod
    def authenticate(self, driver, config: Dict):
        """Authenticate with the LLM service if needed."""
        pass

    @abstractmethod
    def input_query(self, driver, config: Dict, query: str):
        """Input the query to the LLM interface."""
        pass

    @abstractmethod
    def extract_response(self, driver, config: Dict) -> str:
        """Extract the response from the LLM interface."""
        pass

    def run(self, config: Dict, query: str) -> Optional[Tuple[str, str, datetime]]:
        """Run the full automation process."""
        driver = None
        try:
            # Setup browser
            driver = self.setup_driver(config)
            # driver.implicitly_wait(10)

            # Navigate to LLM website
            driver.get(config["url"])
            logger.info(f"Navigated to {config['url']}")

            # Wait for page to load
            time.sleep(10)

            # Authenticate if needed
            self.authenticate(driver, config)

            # Input query
            self.input_query(driver, config, query)
            logger.info(f"Sent query to {self.get_name()}")

            # Wait for response
            wait_time = config.get("wait_time", 60)
            logger.info(
                f"Waiting up to {wait_time} seconds for response from {self.get_name()}"
            )
            time.sleep(config["wait_time"])

            # Extract response
            response_text = self.extract_response(driver, config)
            timestamp = datetime.now()

            logger.info(
                f"Got response from {self.get_name()} ({len(response_text)} chars)"
            )
            return (self.get_name(), response_text, timestamp)

        except TimeoutException:
            logger.error(f"Timeout while waiting for response from {self.get_name()}")
            return None
        except Exception as e:
            logger.exception(f"Error with {self.get_name()}: {str(e)}")
            return None
        finally:
            if driver:
                driver.quit()

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the LLM."""
        pass


class BrowserAutomation:
    """Manager class to handle browser automation for different LLMs."""

    def __init__(self, headless: bool = True):
        self.headless = headless

    async def get_response(
        self, llm_name: str, config: Dict, query: str
    ) -> Optional[Tuple[str, str, datetime]]:
        """
        Get the response from the LLM
        :param llm_name: str: The name of the LLM
        :param config: Dict: The configuration for the LLM
        :param query: str: The query to send to the LLM
        :return: Tuple of (llm_name, response_text, timestamp) if successful, None otherwise.
        """
        return await asyncio.to_thread(
            self._run_browser_automation, llm_name, config, query
        )

    def _run_browser_automation(
        self, llm_name: str, config: Dict, query: str
    ) -> Optional[Tuple[str, str, datetime]]:
        """Run browser automation for the specified LLM."""
        from llms.factory import LLMAutomationFactory

        automation = LLMAutomationFactory.create_automation(llm_name, self.headless)
        return automation.run(config, query)
