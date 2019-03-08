"""
This program reads a list of websites, accesses these websites via Selenium in a headless
instance of Chrome, and attempts to find the zip code and phone on the contact page
cross-referencing a zipcode database to find the city and state. It writes the found
data in a spreadsheet to disk.
"""

import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import numpy as np
import pandas as pd

f = 'websites.csv'
zipdbf = 'zipdb/free-zipcode-database-Primary.csv'  # Zipcode db
zipdb = pd.read_csv(zipdbf, header=0)  # Initializing zipcode db


class SiteToScrape:
    """
    Enables easier storage of site_to_scrape information
    """
    def __init__(self):
        self.website = None
        self.zip = None
        self.city = None
        self.state = None
        self.phone = None

    def __repr__(self):
        return f'{self.website}, {self.zip}, {self.city}, {self.state}, {self.phone}'

    def get_values(self):
        return [self.website, self.zip, self.city, self.state, self.phone]


def start_chrome():
    """
    Initializes a headless instance of Chrome
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(2)

    return driver


def fetch_soup(website, driver):
    """
    Goes to a link and returns the soup, also updates the website to whatever
    the driver is redirected to
    """
    try:
        driver.get(website)
    except (AssertionError, WebDriverException):
        print("Bad link")
        return None, None
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except:
        print("Couldn't load HTML")
        return None, None

    current_url = driver.current_url
    return soup, current_url


def get_contact_link(website, soup):
    """
    Attempts to find contact link on the site_to_scrape's homepage and returns it
    Uses: absolutify_href
    """
    if not soup:
        return None
    atags = soup.find_all('a', href=True)

    for atag in atags:
        href = atag['href'].lower()
        atag_text = atag.text.lower()
        if ('contact' in href or 'contact' in atag_text):
            if href[0] == '/':
                href = href[1:]

            return absolutify_href(website, href)

    for atag in atags:
        href = atag['href'].lower()
        atag_text = atag.text.lower()
        if ('about' in href or 'about' in atag_text):
            if href[0] == '/':
                href = href[1:]

            return absolutify_href(website, href)

    return None


def absolutify_href(link, href):
    """
    Makes a relative url into an absolute url
    """
    if link[-1] == '/':
        link = link[:-1]

    link_parts = link.split('/')[2:]
    href_parts = href.split('/')

    if 'http' in href_parts[0]:
        return href

    # Joins website and href paths together if there is an overlap
    for i, part in enumerate(link_parts):
        if part == href_parts[0]:
            return 'https://' + '/'.join(link_parts[:-i]) + '/' + '/'.join(href_parts)

    return 'https://' + '/'.join(link_parts) + '/' + '/'.join(href_parts)


def get_zip_city(soup):
    """
    Attempts to find a zipcode on a website, if found returns the zip code and the city
    Uses: zip_to_place
    """
    # Removes script, style, and noscript elements
    # There were a lot of false positives in the scripts and styles tags, since they
    # use many 5 digit numbers for ids, colors, etc.
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')]
    [x.extract() for x in soup.find_all('noscript')]

    try:
        if not soup:
            return None, None, None
        if soup.find('body'):
            lex = soup.find('body').text
        else:
            lex = soup.text
        # " AA  ddddd " is a lot more likely to be a zip than " ddddd "
        zip_explicits = re.findall(r'\s([a-zA-z]{2}\s\d{5})\D', lex)
        for zip_explicit in zip_explicits:
            city, state = zip_to_place(zip_explicit[-5:])
            if city:
                return zip_explicit[-5:], city, state

    except (TypeError, TimeoutError):  # Cookies failed to delete themselves
        pass

    return None, None, None


def get_phone(soup):
    """
    Finds phone number on page
    """
    # Removes script, style, and noscript elements
    # There were a lot of false positives in the scripts and styles tags, since they
    # use many 5 digit numbers for ids, colors, etc.
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')]
    [x.extract() for x in soup.find_all('noscript')]

    try:
        if not soup:
            return None
        phones = re.findall(r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', soup.text)
        if phones:
            return phones[0].strip()
        else:
            return None
    except TypeError:
        return None


def zip_to_place(code):
    """
    Checks zipcode against zipcode database
    """
    try:
        place = zipdb[zipdb['Zipcode'] == int(code)][['City', 'State']]
        place = place.values.tolist()[0]

        if place:
            return place[0], place[1]

    except (TypeError, IndexError):
        return None, None


def main():
    loaded_data = pd.read_csv(f)

    websites = loaded_data['Website']
    for i, website in enumerate(websites):
        if website:
            if website[:4] != 'http':
                website = 'https://' + website
        websites[i] = website

    # Attempting to find zipcode and city from the website, then storing it into the site_to_scrape object
    driver = start_chrome()
    data_out = pd.DataFrame(
        index=range(1000), columns=['Website', 'Zipcode', 'City', 'State', 'Phone', 'Time']
    )
    t0 = time.time()
    g = 'Found_zips.csv'

    for i, website in enumerate(websites):
        site_to_scrape = SiteToScrape()
        site_to_scrape.website = website
        t1 = time.time()
        soup, site_to_scrape.website = fetch_soup(site_to_scrape.website, driver)
        contact_link = get_contact_link(site_to_scrape.website, soup)

        if contact_link:
            try:
                contact_soup = fetch_soup(contact_link, driver)[0]
                site_to_scrape.zip, site_to_scrape.city, site_to_scrape.state = (get_zip_city(contact_soup))
                site_to_scrape.phone = get_phone(contact_soup)
            except:
                driver.quit()
                driver = start_chrome()

        if not site_to_scrape.zip:
            # If zipcode already on frontpage, grabs it
            try:
                site_to_scrape.zip, site_to_scrape.city, site_to_scrape.state = (get_zip_city(soup))
                site_to_scrape.phone = get_phone(soup)
            except:
                driver.quit()
                driver = start_chrome()

        t2 = time.time()
        print(f'{i+1} of {len(websites)} done.')
        print(f'Took: {np.round(t2-t1, 1)}, Total Time: {np.round(t2-t0,1)}, {site_to_scrape}')

        data_out.iloc[i % 1000, :] = site_to_scrape.get_values() + [pd.Timestamp.now()]

        # Saves every 10 times
        if (i + 1) % 10 == 0:
            data_out.to_csv(g, index=False)
            print("Progress saved")

        # Creates new file every 1000 times (limits memory use)
        if (i + 1) % 1000 == 0:
            g = f'Found_zips{i+1}.csv'
            data_out = pd.DataFrame(
                index=range(1000), columns=['Website', 'Zipcode', 'City', 'State', 'Phone', 'Time']
            )

        driver.delete_all_cookies()  # Limits memory use

    data_out.to_csv(g, index=False)
    print("Progress saved")

if __name__ == "__main__":
    main()
