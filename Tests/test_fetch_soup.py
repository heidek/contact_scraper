from bs4 import BeautifulSoup
import pytest
from selenium import webdriver
from website_scraper.website_scraper import fetch_soup


class TestClass:
    def test_null(self):
        x = None
        assert fetch_soup(x, webdriver.Chrome()) == (None, None)

    def test_negative_no_site(self):
        x = 'notalink'
        assert fetch_soup(x, webdriver.Chrome()) == (None, None)

    def test_positive(self):
        x = 'https://github.com/'
        assert len(fetch_soup(x, webdriver.Chrome())[0].text) > 1000
