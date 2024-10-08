import time
from logging import getLogger

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException


class Browser:
    def __init__(self):
        self._logger = getLogger()
        self._outer_logger = getLogger("outer")
        self._initialization_timeout = 30
        self._driver = None
        self._initialize_browser()

    def _initialize_browser(self):
        """
        Инициализирует веб-браузер Firefox с заданными настройками и профилем.
        """
        start = time.time()
        while time.time() - start < self._initialization_timeout:
            try:
                firefox_options = Options()
                firefox_options.add_argument('--headless')
                self._driver = webdriver.Firefox(options=firefox_options)
                return
            except (WebDriverException, ValueError):
                time.sleep(0.3)

        self._logger.error(f"Driver initialization timeout reached.")

    def close_browser(self):
        """
        Закрывает веб-браузер, если он был открыт.
        """
        if self._driver:
            self._driver.quit()
            self._driver = None

    @property
    def driver(self) -> webdriver.Firefox:
        assert isinstance(self._driver, webdriver.Firefox)
        return self._driver
