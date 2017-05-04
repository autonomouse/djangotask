import os
import sys
import unittest
from selenium import webdriver
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from config import PRIMARY_APP_NAME


class WebDriverTestCase(unittest.TestCase):
    HOST = 'http://127.0.0.1:8000/'
    chromedriver = os.path.join(currentdir, "chromedriver")
    os.environ["webdriver.chrome.driver"] = chromedriver

    def setUp(self):
        # start_django_runserver()  # FIXME: Can I use asyncio for this?
        self.driver = webdriver.Chrome(self.chromedriver)

    def go_to_url(self, url):
        self.driver.get(url)

    def click(self, locator):
        self.driver.find_element_by_css_selector(locator).click()

    def text_entry(self, locator, keys):
        self.driver.find_element_by_css_selector(locator).click()
        self.driver.find_element_by_css_selector(locator).clear()
        self.driver.find_element_by_css_selector(locator).send_keys(keys)

    def tearDown(self):
        self.driver.close()


class FunctionalTests(WebDriverTestCase):
    """ Call from cli by: py.test ./tests/functional_tests.py -v"""
    def test_basic(self):
        self.go_to_url(self.HOST)
        assert PRIMARY_APP_NAME in self.driver.title


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weebl.settings")
    unittest.main()
