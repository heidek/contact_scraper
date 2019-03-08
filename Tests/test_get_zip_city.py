from bs4 import BeautifulSoup
import pytest
from website_scraper.website_scraper import get_zip_city, zip_to_place

f = 'zipdb/free-zipcode-database-Primary.csv'


class TestClass:
    def test_null(self):
        x = BeautifulSoup('', 'html.parser')
        assert get_zip_city(x) == (None, None, None)

    def test_negative(self):
        x = BeautifulSoup('notazip', 'html.parser')
        assert get_zip_city(x) == (None, None, None)

    def test_positive(self):
        x = BeautifulSoup(' NY 12345 ', 'html.parser')
        assert get_zip_city(x) == ('12345', 'SCHENECTADY', 'NY')
