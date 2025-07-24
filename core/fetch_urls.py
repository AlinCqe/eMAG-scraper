from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementClickInterceptedException

import time
import re

class Driver:

    def __init__(self, search_item):
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("window-size=1920,1080")
        self.search_item = search_item
        self.search_item_formated = self.search_item.strip().replace(' ', '+')
        self.driver =  webdriver.Chrome(options=self.options )
        self.wait = WebDriverWait(self.driver, 10)

        self.first_hidden_api = None
        self.second_hidden_api = None

    def first_api_fetch(self):

        self.driver.requests.clear()

        self.driver.get(f'https://www.emag.ro/search/{self.search_item_formated}')

        # Gets the first hidden api 
        while not self.first_hidden_api:

            self.first_hidden_api = self.get_url_from_requests(self.driver.requests, prefix='https://sapi.emag.ro/recommendations/by-zone-by-filters')

            # if it wasnt able to get first api reload the page 
            if not self.first_hidden_api:
                print('Reloading first page')
                self.driver.refresh()
                time.sleep(1)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'has-chat-button')))

        print('Firts URL caught')

        self.first_hidden_api = self.set_page_limit_to_100(self.first_hidden_api)

        return self.first_hidden_api


    def second_api_fetch(self):

        self.driver.requests.clear()


        for _ in range(5):

            # Try closing a info popup
            try:
                info_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'fs-12.btn.btn-primary.btn-block.js-accept.gtm_h76e8zjgoo')))
                info_button.click()
                print('Passed info popup - clicked')
            except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException):
                print('Passed info popup - passed')
                


            # Try closing cookies popup
            try:
                cookies_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'btn.btn-primary.btn-block.js-accept.gtm_h76e8zjgoo')))
                cookies_button.click()
                print('Passed cookies popup - clicked')
            except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException):
                print('Passed cookies popup - passed')
                

            # Try closing login popup
            try:
                login_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'js-dismiss-login-notice-btn.dismiss-btn.btn.btn-link.py-0.px-0')))
                login_button.click()
                print('Passed login popup - clicked')
            except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException):
                print('Passed login popup - passed')
                



            # Try clicking next page button
            try:
                self.driver.requests.clear()
                next_page_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']")))
                next_page_button.click()
                time.sleep(1.4)
                print('Going to the next page')

            # Next page button may be blocker - reload the page an try again
            except ElementClickInterceptedException:

                print('Something was blocking the button, reloading the page')
                self.driver.requests.clear()
                self.driver.refresh()
                time.sleep(1)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'has-chat-button')))
                

            except TimeoutException:
                print('Next page button wasnt found')
                self.driver.close()
                return None

            self.second_hidden_api = self.get_url_from_requests(self.driver.requests, prefix='https://www.emag.ro/search-by-url?source_id=')

            if self.second_hidden_api:
                self.driver.close()
                print('Second URL caught')
                return self.second_hidden_api   
                



    def set_page_limit_to_100(self, word):
        return re.sub(r'page%5Boffset%5D=0&page%5Blimit%5D=\d{1,3}', 'page%5Boffset%5D=0&page%5Blimit%5D=100', word)


    def get_url_from_requests(self, requests_list, prefix):
        for request in requests_list:

            if not request.response:
                continue

            if request.url.startswith(prefix):

                url = f'{request.url}'
                self.driver.requests.clear()

                return url
        return None