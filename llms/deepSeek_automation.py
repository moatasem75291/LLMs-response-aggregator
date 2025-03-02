from typing import Dict
import logging
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from core.browser import LLMBrowserAutomation

logger = logging.getLogger(__name__)


class DeepSeekAutomation(LLMBrowserAutomation):
    """Implementation for DeepSeek browser automation."""

    def get_name(self) -> str:
        return "deepseek"

    def setup_driver(self, config: Dict):
        logger.info(f"Starting browser for {self.get_name()}")
        return uc.Chrome(options=self.get_chrome_options())

    def authenticate(self, driver, config: Dict):
        # Login process for DeepSeek
        email_field = WebDriverWait(driver, config["wait_time_for_logging"]).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Phone number / email address']")
            )
        )
        email_field.send_keys(config["email"])

        password_field = driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Password']"
        )
        password_field.send_keys(config["password"])

        checkbox = driver.find_element(By.CSS_SELECTOR, ".ds-checkbox")
        checkbox.click()

        login_button = driver.find_element(
            By.CSS_SELECTOR, "div.ds-button.ds-button--primary.ds-button--filled"
        )
        ActionChains(driver).move_to_element(login_button).click().perform()

        # Wait for login to complete
        WebDriverWait(driver, config["wait_time_for_logging"]).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, config["input_selector"]))
        )

    def input_query(self, driver, config: Dict, query: str):
        input_box = driver.find_element(By.CSS_SELECTOR, config["input_selector"])
        input_box.send_keys(query)
        input_box.send_keys(Keys.RETURN)

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
