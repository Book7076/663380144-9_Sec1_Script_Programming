import logging
from typing import Optional
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    ChromeDriverManager = None


logger = logging.getLogger(__name__)


class DriverManager:
    """Creates and closes a Selenium Chrome WebDriver."""

    def __init__(self, browser_name: str = "chrome", headless: bool = True):
        self.browser_name = browser_name.lower()
        self.headless = headless
        self.driver = None

    def _resolve_chromedriver_path(self) -> Optional[str]:
        """Resolve chromedriver executable path, fixing webdriver-manager bug if needed."""
        if ChromeDriverManager is None:
            return None
        try:
            raw_path = ChromeDriverManager().install()
            path_obj = Path(raw_path)
            if path_obj.is_file():
                if path_obj.suffix.lower() == ".exe":
                    return str(path_obj)
                # webdriver-manager known bug: may pick THIRD_PARTY_NOTICES.chromedriver
                candidate = path_obj.parent / "chromedriver.exe"
                if candidate.exists():
                    return str(candidate)
            elif path_obj.is_dir():
                candidate = path_obj / "chromedriver.exe"
                if candidate.exists():
                    return str(candidate)
            return raw_path
        except Exception as e:
            logger.warning("webdriver-manager resolution failed: %s", e)
            return None

    def get_driver(self):
        """Initialize Chrome and return the WebDriver."""
        if self.driver is not None:
            return self.driver

        if self.browser_name != "chrome":
            raise ValueError("This project currently supports Chrome only.")

        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-notifications")
        options.add_argument("--log-level=3")

        # 1. Try ChromeDriverManager with path resolution (produces WebDriver manager logs like expected in lab)
        try:
            driver_path = self._resolve_chromedriver_path()
            service = ChromeService(executable_path=driver_path) if driver_path else ChromeService()
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.implicitly_wait(2)
            self.driver.set_page_load_timeout(30)
            logger.info("Chrome WebDriver started successfully.")
            return self.driver
        except Exception as dm_err:
            logger.warning("WebDriver manager failed (%s). Trying Selenium Manager fallback...", dm_err)

        # 2. Fallback to Selenium Manager (built into Selenium 4.6+)
        try:
            self.driver = webdriver.Chrome(service=ChromeService(), options=options)
            self.driver.implicitly_wait(2)
            self.driver.set_page_load_timeout(30)
            logger.info("Chrome WebDriver started successfully.")
            return self.driver
        except Exception:
            logger.exception(
                "Could not start Chrome. Check that Google Chrome is installed "
                "and that the computer can download the matching driver."
            )
            self.quit_driver()
            return None

    def quit_driver(self) -> None:
        """Close the browser if it is running."""
        if self.driver is not None:
            try:
                self.driver.quit()
                logger.info("Chrome WebDriver closed.")
            except Exception:
                logger.exception("An error occurred while closing Chrome.")
            finally:
                self.driver = None