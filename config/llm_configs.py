from typing import List, Dict
import os
import dotenv

dotenv.load_dotenv()

"""Configuration settings for supported LLMs."""

LLM_CONFIGS = {
    "chatgpt": {
        "url": "https://chat.openai.com/",
        "input_selector": "div.ProseMirror",
        "response_selector": "div.markdown.prose",
        "wait_time": 20,  # seconds
    },
    "mistral": {
        "url": "https://chat.mistral.ai/chat/",
        "input_selector": "textarea.border-input",
        "response_selector": '(//div[contains(@class, "prose")])[last()]',
        "wait_time": 20,
    },
    "grok": {
        "url": "https://grok.com/",
        "input_selector": "textarea.w-full.px-2",
        "response_selector": "div.message-bubble.prose",
        "wait_time": 20,
    },
    "deepseek": {
        "url": "https://chat.deepseek.com/",
        "email": os.getenv("DEEPSEEK_EMAIL"),
        "password": os.getenv("DEEPSEEK_PASSWORD"),
        "input_selector": "textarea.c92459f0",
        "response_selector": "div.ds-markdown",
        "wait_time_for_logging": 5,
        "wait_time": 20,
    },
}


def get_llm_configs(llm_name: str) -> Dict:
    """Get the configuration for a given LLM."""

    return LLM_CONFIGS.get(llm_name)


def get_available_llms() -> List[str]:
    """Get the list of available LLMs."""

    return list(LLM_CONFIGS.keys())
