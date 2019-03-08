import pytest
from website_scraper.website_scraper import zip_to_place

f = 'zipdb/free-zipcode-database-Primary.csv'


class TestClass:
    def test_null(self):
        x = None
        assert zip_to_place(x) == (None, None)

    def test_negative(self):
        x = '0000000'
        assert zip_to_place(x) == (None, None)

    def test_positive(self):
        x = '12345'
        assert zip_to_place(x) == ('SCHENECTADY', 'NY')
