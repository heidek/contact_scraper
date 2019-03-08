import pytest
import selenium
from website_scraper.website_scraper import start_chrome


class TestClass(object):
        def test_init(self):
            x = selenium.webdriver.chrome.webdriver.WebDriver
            assert isinstance(start_chrome(), x)
