# Scraper for Stockanalysis.com
import os
import time

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Excel imports
from Excel.excel import Excel

# Numbers
import numpy as np
import pandas as pd


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--headless") NOTE: Running in headless will result in empty dataframes.
chrome_options.add_argument("--disable-gpu")


class LlamaScraper:
    def __init__(
        self,
        driver_path: str = "D:\\Chromedriver\\chromedriver.exe",
        dataset_path: str = "D:\\DEFILLAMA",
    ) -> None:
        self.chrome_driver = driver_path
        self.dataset_path = dataset_path
        self.excel = Excel()

    def create_browser(self, url=None):
        """
        :param url: The website to visit.
        :return: None
        """
        service = Service(executable_path=self.chrome_driver)
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        # Default browser route
        if url == None:
            self.browser.get(url=self.sec_quarterly_url)
        # External browser route
        else:
            self.browser.get(url=url)

    def read_data(self, xpath: str, wait: bool = False, wait_time: int = 5) -> str:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: (str) Text of the element.
        """

        if wait:
            data = WebDriverWait(self.browser, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        else:
            data = self.browser.find_element("xpath", xpath)
        # Return the text of the element found.
        return data.text

    def click_button(self, xpath: str, wait: bool = False, wait_time: int = 5) -> None:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: None. Because this function clicks the button but does not return any information about the button or any related web elements.
        """

        if wait:
            element = WebDriverWait(self.browser, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        else:
            element = self.browser.find_element("xpath", xpath)
        element.click()

    def clean_close(self) -> None:
        self.browser.close()
        self.browser.quit()

    def scroll_page(self, pixel_count: int = 1000) -> None:
        # Scroll down by a certain amount (e.g., 1000 pixels)
        self.browser.execute_script(f"window.scrollBy(0, {pixel_count});")

    def scroll_to_element(self, val, method: str = "XPATH", sleeptime: int = 2) -> None:
        if method.upper() == "XPATH":
            self.browser.find_element(By.XPATH, val).send_keys(Keys.END)
            time.sleep(sleeptime)

    """
    ==================================
    Value Formatting
    ==================================
    """

    def format_dollar(self, val) -> float:
        magnitudes = ["m", "b", "t"]
        # Remove dollar sign from string if present.
        if "$" in val:
            val = val.replace("$", "")

        # Remove commas from string if present.
        if "," in val:
            val = val.replace(",", "")

        try:
            magnitude = val[-1]

            if magnitude in magnitudes:
                val = val[:-1]  # Remove suffix.
                if magnitude.lower() == "m":
                    multi = 1_000_000
                elif magnitude.lower() == "b":
                    multi = 1_000_000_000
                elif magnitude.lower() == "t":
                    multi = 1_000_000_000_000

                val = float(val) * multi

            try:
                return int(val)
            except ValueError:
                return float(val)
        except IndexError:
            return np.nan

    def format_basic(self, val) -> int:
        magnitudes = ["m", "b", "t"]
        # Remove commas from string if present.
        if "," in val:
            val = val.replace(",", "")

        try:
            magnitude = val[-1]
            if magnitude in magnitudes:
                val = val[:-1]  # Remove suffix.
                if magnitude.lower() == "m":
                    multi = 1_000_000
                elif magnitude.lower() == "b":
                    multi = 1_000_000_000
                elif magnitude.lower() == "t":
                    multi = 1_000_000_000_000

                val = int(float(val) * multi)

            return val
        except IndexError:
            return np.nan

    """
    ==================================
    Value Formatting
    ==================================
    """
    """
    ==================================
    Value Formatting
    ==================================
    """
