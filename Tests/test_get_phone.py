from bs4 import BeautifulSoup
import pytest
from website_scraper.website_scraper import get_phone


class TestClass:
    def test_null(self):
        x = BeautifulSoup('', 'html.parser')
        assert get_phone(x) is None

    def test_negative(self):
        x = BeautifulSoup('12345', 'html.parser')
        assert get_phone(x) is None

    def test_positive(self):
        test_list = ['123-123-1234', '1231231234', '123.123.1234', '123 123 1234', '(123)123 1234', '(123)-123-1234']
        for number in test_list:
            x = BeautifulSoup(number, 'html.parser')
            assert get_phone(x) == number
