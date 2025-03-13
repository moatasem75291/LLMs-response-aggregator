from typing import Dict
import logging
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from core.browser import LLMBrowserAutomation

logger = logging.getLogger(__name__)


class GrokAutomation(LLMBrowserAutomation):
    """Grok implementation for other LLM browser automation."""

    def __init__(self, llm_name: str, headless: bool = True):
        super().__init__(headless)
        self.llm_name = llm_name

    def get_name(self) -> str:
        return self.llm_name

    def setup_driver(self, config: Dict):
        logger.info(f"Starting browser for {self.get_name()}")
        service = Service(ChromeDriverManager().install())
        return uc.Chrome(service=service, options=self.get_chrome_options())

    def authenticate(self, driver, config: Dict):
        # Grok LLM doesn't need authentication in this implementation
        pass

    def input_query(self, driver, config: Dict, query: str):
        WebDriverWait(driver, config["wait_time"]).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, config["input_selector"]))
        )

        input_field = driver.find_element(By.CSS_SELECTOR, config["input_selector"])
        try:
            input_field.clear()
        except:
            # If clear fails, just continue
            pass

        input_field.send_keys(query)
        input_field.send_keys(Keys.RETURN)

    def extract_response(self, driver, config: Dict) -> str:
        response_elements = driver.find_elements(
            By.CSS_SELECTOR, config["response_selector"]
        )
        if not response_elements:
            logger.warning(f"No response elements found for {self.get_name()}")
            return ""

        # Get the last response element (most recent)
        response_text = response_elements[-1].text

        # If response is empty, wait and try again
        if not response_text.strip():
            logger.info("Empty response, waiting longer...")
            time.sleep(10)
            response_elements = driver.find_elements(
                By.CSS_SELECTOR, config["response_selector"]
            )
            if response_elements:
                response_text = response_elements[-1].text

        return response_text
