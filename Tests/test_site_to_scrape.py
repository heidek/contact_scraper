import pytest
from website_scraper import SiteToScrape


class TestSiteToScrape:
    def test_repr(self):
        x = SiteToScrape()
        x.website = 'test.com'
        x.zipcode = '12345'
        x.city = 'Schenectady'
        x.state = 'New York'
        x.phone = '555-555-5555'
        assert str(x) == 'test.com, 12345, Schenectady, New York, 555-555-5555'
