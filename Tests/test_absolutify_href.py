import pytest
from website_scraper.website_scraper import absolutify_href


class TestClass:
    def test_link(self):
        x1 = 'http://google.com'
        x2 = 'about-us'
        assert absolutify_href(x1, x2) == 'https://google.com/about-us'
