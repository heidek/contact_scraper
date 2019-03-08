from bs4 import BeautifulSoup
import pytest
from selenium import webdriver
from website_scraper.website_scraper import get_contact_link


class TestClass:
    def test_null(self):
        x = None
        assert get_contact_link(x, x) is None

    def test_badlink(self):
        x = 'https://notalink'
        driver = webdriver.Chrome()
        driver.get(x)
        x_bs = BeautifulSoup(driver.page_source, 'html.parser')
        assert get_contact_link(x, x_bs) is None

    def test_negative(self):
        x = 'https://sites.math.washington.edu/~mcgovern/508.html'
        driver = webdriver.Chrome()
        driver.get(x)
        x_bs = BeautifulSoup(driver.page_source, 'html.parser')
        assert get_contact_link(x, x_bs) is None

    def test_positive_about(self):
        x = 'https://tenhou.net/'
        driver = webdriver.Chrome()
        driver.get(x)
        x_bs = BeautifulSoup(driver.page_source, 'html.parser')
        assert get_contact_link(x, x_bs) == 'https://tenhou.net/about_shop.html'

    def test_positive_contact(self):
        x = 'https://github.com/'
        driver = webdriver.Chrome()
        driver.get(x)
        x_bs = BeautifulSoup(driver.page_source, 'html.parser')
        assert get_contact_link(x, x_bs) == 'https://enterprise.github.com/contact'
