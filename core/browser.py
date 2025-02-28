import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional, Tuple
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


logger = logging.getLogger(__name__)


class BrowserAutomation:
    def __init__(self, headless: bool = True):
        """
        Initialize the browser automation class
        :param headless: bool: True if the browser should be headless
        """
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

    # Update the _run_browser_automation method in llm_aggregator/core/browser.py

    def _run_browser_automation(
        self, llm_name: str, config: Dict, query: str
    ) -> Optional[Tuple[str, str, datetime]]:
        """Run browser automation to interact with an LLM website."""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = None
        try:
            logger.info(f"Starting browser for {llm_name}")
            driver = webdriver.Chrome(options=options)

            # Set an implicit wait for all operations
            driver.implicitly_wait(10)

            # Navigate to the LLM website
            driver.get(config["url"])
            logger.info(f"Navigated to {config['url']}")

            # Add a sleep to ensure page is fully loaded
            time.sleep(15)

            # Wait for the page to load
            if llm_name == "chatgpt":
                time.sleep(35)
                # Special handling for ChatGPT
                # container_selector = "div._prosemirror-parent_1r7mb_1"
                WebDriverWait(driver, config["wait_time"]).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, config["input_selector"])
                    )
                )

                # Click on the container to focus it
                container = driver.find_element(
                    By.CSS_SELECTOR, config["input_selector"]
                )
                ActionChains(driver).move_to_element(container).click().perform()

                # Send keys to the active element (the focused editor)
                container.send_keys(query)
                container.send_keys(Keys.RETURN)
            else:
                # Regular handling for other LLMs
                WebDriverWait(driver, config["wait_time"]).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, config["input_selector"])
                    )
                )

                # Find the input field, enter the query, and send it
                input_field = driver.find_element(
                    By.CSS_SELECTOR, config["input_selector"]
                )
                try:
                    input_field.clear()
                except:
                    # If clear fails, just continue
                    pass

                input_field.send_keys(query)
                input_field.send_keys(Keys.RETURN)

            logger.info(f"Sent query to {llm_name}")

            # IMPORTANT: Wait for the response with a much longer timeout
            wait_time = config.get(
                "wait_time", 60
            )  # Default to 60 seconds if not specified
            logger.info(
                f"Waiting up to {wait_time} seconds for response from {llm_name}"
            )

            # Add additional delay to ensure response is complete
            logger.info(
                f"Response element found, waiting for content generation to complete"
            )
            time.sleep(10)  # Wait an additional 10 seconds for full response generation

            # Extract the response
            response_elements = driver.find_elements(
                By.CSS_SELECTOR, config["response_selector"]
            )
            if not response_elements:
                logger.warning(f"No response elements found for {llm_name}")
                return None

            # Get the last response element (most recent)
            response_text = response_elements[-1].text

            # If response is empty, wait a bit longer and try again
            if not response_text.strip():
                logger.info("Empty response, waiting longer...")
                time.sleep(10)
                response_elements = driver.find_elements(
                    By.CSS_SELECTOR, config["response_selector"]
                )
                if response_elements:
                    response_text = response_elements[-1].text

            timestamp = datetime.now()

            logger.info(f"Got response from {llm_name} ({len(response_text)} chars)")
            return (llm_name, response_text, timestamp)

        except TimeoutException:
            logger.error(f"Timeout while waiting for response from {llm_name}")
            return None
        except Exception as e:
            logger.exception(f"Error with {llm_name}: {str(e)}")
            return None
        finally:
            if driver:
                driver.quit()
