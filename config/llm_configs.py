from typing import List, Dict

"""Configuration settings for supported LLMs."""

LLM_CONFIGS = {
    "chatgpt": {
        "url": "https://chat.openai.com/",
        "input_selector": "div.ProseMirror",
        "response_selector": "div.markdown.prose",
        "wait_time": 30,  # seconds
    },
    "mistral": {
        "url": "https://chat.mistral.ai/chat/",
        "input_selector": "textarea.border-input",
        "response_selector": "div.prose.select-text",
        "wait_time": 50,
    },
    "grok": {
        "url": "https://grok.com/",
        "input_selector": "textarea.w-full.px-2",
        "response_selector": "div.message-bubble.prose",
        "wait_time": 50,
    },
}


def get_llm_configs(llm_name: str) -> Dict:
    """Get the configuration for a given LLM."""

    return LLM_CONFIGS.get(llm_name)


def get_available_llms() -> List[str]:
    """Get the list of available LLMs."""

    return list(LLM_CONFIGS.keys())
