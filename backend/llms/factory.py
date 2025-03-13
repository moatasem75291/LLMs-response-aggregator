"""Factory for creating LLM automation instances."""

from core.browser import LLMBrowserAutomation


class LLMAutomationFactory:
    """Factory for creating LLM automation instances."""

    @staticmethod
    def create_automation(llm_name: str, headless: bool = True) -> LLMBrowserAutomation:
        """Create an appropriate LLM automation instance based on the LLM name."""
        llm_name = llm_name.strip().lower()

        if llm_name == "chatgpt":
            from llms.chatGPT_automation import ChatGPTAutomation

            return ChatGPTAutomation(headless)
        elif llm_name == "deepseek":
            from llms.deepSeek_automation import DeepSeekAutomation

            return DeepSeekAutomation(headless)

        elif llm_name == "mistral":
            from llms.mistral_automation import MistralAutomation

            return MistralAutomation(llm_name, headless)
        elif llm_name == "grok":
            from llms.grok_automation import GrokAutomation

            return GrokAutomation(llm_name, headless)
