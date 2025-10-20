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
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("window-size=1920,1080")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")


        self.search_item = search_item
        self.search_item_formated = self.search_item.strip().replace(' ', '+')

                
        self.driver = webdriver.Chrome(
            options=self.options,
            seleniumwire_options={
                'port': 12345,       
                'verify_ssl': False,  
            }
        )
        self.wait = WebDriverWait(self.driver, 15)

        self.driver.scopes = ['.*']  
        self.driver.proxy.verify_ssl = False
        
        self.first_hidden_api = None
        self.second_hidden_api = None

    def first_api_fetch(self):

        """"

        Gets the first end point from which eMAG fetches items data based on a search item
        Uses selenium-wire to monitor network requests and look for a specific API endpoint.

        If the URL isnt found, it refreshes the page and retries until its caught

        """

        self.driver.requests.clear()

        self.driver.get(f'https://www.emag.ro/search/{self.search_item_formated}')

        while not self.first_hidden_api:

            self.first_hidden_api = self.get_url_from_requests(self.driver.requests, prefix='https://sapi.emag.ro/recommendations/by-zone-by-filters')

            if not self.first_hidden_api:
                print('Reloading first page')
                self.driver.refresh()
                time.sleep(1)

                try:
                    WebDriverWait(self.driver, 20).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )
                    print("Page fully loaded!")
                except TimeoutException:
                    print("⚠️ Page load timeout — proceeding anyway")

        print('Firts URL caught')

        self.first_hidden_api = self.set_page_limit_to_100(self.first_hidden_api)

        return self.first_hidden_api


    def second_api_fetch(self):

        """"
        Gets the second endpoint used by eMAG to fetch item data
        This API is typically triggered when navigating to the second page of results

        The function:
        - Tries to close common popups (info, cookies, login)
        - Tries to go to the next page up to 5 times
        - If there's no "Next" button, it assumes there is no second page
        - If the button exists but is blocked, it refreshes and retries
        - Once the second API is detected in the requests, it returns the URL

        If not found after all retries, it returns None.
        """

        self.driver.requests.clear()

        for _ in range(5):

            self.click_button(path='fs-12.btn.btn-primary.btn-block.js-accept.gtm_h76e8zjgoo', button_name='info popup')

            self.click_button(path='btn.btn-primary.btn-block.js-accept.gtm_h76e8zjgoo', button_name='cookies popup')

            self.click_button(path='js-dismiss-login-notice-btn.dismiss-btn.btn.btn-link.py-0.px-0', button_name='login popup')

            # Attempt to click next page button
            try:
                self.driver.requests.clear()
                next_page_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']")))
                next_page_button.click()
                time.sleep(1.4)
                print('Going to the next page')
            
            # Retry in case an element is blocking the button
            except ElementClickInterceptedException:

                print('Something was blocking the next page button, reloading the page')
                self.driver.requests.clear()
                self.driver.refresh()
                time.sleep(1)
                
                try:
                    WebDriverWait(self.driver, 20).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )
                    print("Page fully loaded!")
                except TimeoutException:
                    print("⚠️ Page load timeout — proceeding anyway")

                
            # If no "Next" button is found, there's probably only one page
            except TimeoutException:
                print('Next page button wasnt found')
                self.driver.close()
                return None

            self.second_hidden_api = self.get_url_from_requests(self.driver.requests, prefix='https://www.emag.ro/search-by-url?source_id=')

            if self.second_hidden_api:
                
                self.driver.close()
                return self.second_hidden_api   
                



    def set_page_limit_to_100(self, word):
        """
        Given a URL, replaces the default page limit with 100 items per page
        """

        return re.sub(r'page%5Boffset%5D=0&page%5Blimit%5D=\d{1,3}', 'page%5Boffset%5D=0&page%5Blimit%5D=100', word)


    def get_url_from_requests(self, requests_list, prefix):

        """
        Iterates through the browsers request list and returns the first URL that starts with a specific prefix
        """
        

        for request in requests_list:

            if not request.response:
                continue

            if request.url.startswith(prefix):

                url = f'{request.url}'
                self.driver.requests.clear()

                return url
        return None
    
    def click_button(self, path, button_name):

        """
        Attempts to click a popup close button based on a class name
        Logs the result with the buttons purpose (e.g. cookies, login)
        """

        try:
            cookies_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME , path)))
            cookies_button.click()
            print(f'Passed {button_name} - clicked')
        except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException):
            print(f'Passed {button_name} - didnt appear')
            
