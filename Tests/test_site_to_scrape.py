import pytest
from website_scraper.website_scraper import SiteToScrape


class TestClass:
    def test_repr(self):
        x = SiteToScrape()
        x.website = 'test.com'
        x.zip = '12345'
        x.city = 'Schenectady'
        x.state = 'New York'
        x.phone = '555-555-5555'
        assert str(x) == 'test.com, 12345, Schenectady, New York, 555-555-5555'

    def test_get_values(self):
        x = SiteToScrape()
        x.website = 'test.com'
        x.zip = '12345'
        x.city = 'Schenectady'
        x.state = 'New York'
        x.phone = '555-555-5555'
        assert x.get_values() == ['test.com', '12345', 'Schenectady', 'New York', '555-555-5555']
