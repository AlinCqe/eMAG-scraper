from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementClickInterceptedException

import time


class Driver:

    def __init__(self, search_item):
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("window-size=1920,1080")
        self.search_item = search_item
        self.driver =  webdriver.Chrome(options=self.options )
        self.wait = WebDriverWait(self.driver, 10)

    def start_driver(self):
        self.search_item_formated = self.search_item.strip().replace(' ', '+')
        self.driver.get(f'https://www.emag.ro/search/{self.search_item_formated}')


    def first_api_fetch(self):
        self.driver.requests.clear()
        first_hidden_api = None
        # Gets the first hidden api 
        while not first_hidden_api:
            for request in self.driver.requests:
                if request.response:
                    if request.url.startswith('https://sapi.emag.ro/recommendations/by-zone-by-filters'):
                        first_hidden_api = f'{request.url}'
                        print('Firts URL caught')
                        break
            if not first_hidden_api:
                print('Reloading first page')
                self.driver.refresh()
                time.sleep(1)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'has-chat-button')))

        # Set the page items limit to max so we dont have to loop trought the same page
        suffix = f'page%5Boffset%5D=0&page%5Blimit%5D=12'
        first_hidden_api = first_hidden_api.replace(suffix, f'page%5Boffset%5D=0&page%5Blimit%5D=100')
        self.driver.requests.clear()
        return first_hidden_api



    def second_api_fetch(self):

        for _ in range(5):
            for request in self.driver.requests:
                if request.response and request.response.status_code == 200:
                    if request.url.startswith('https://www.emag.ro/search-by-url?source_id='):
                        second_hidden_api = f'{request.url}'
                        print('Second URL caught')
                        return second_hidden_api       

            # Try clicking the cookies thing
            try:
                firts_cookies_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'btn.btn-primary.btn-block.js-accept.gtm_h76e8zjgoo')))
                firts_cookies_button.click()
            except (StaleElementReferenceException,TimeoutException,ElementClickInterceptedException):
                print('Could not click "Cookies" button')
                continue

            # Try closing the login thing
            try:
                close_login_notif_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'js-dismiss-login-notice-btn.dismiss-btn.btn.btn-link.py-0.px-0')))
                close_login_notif_button.click()
            except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException):
                print('Could not click "Close login" button')
                continue

            # Try clicking next page button
            try:
                self.driver.requests.clear()
                next_page_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']")))
                next_page_button.click()
                print('Going to the next page')
            except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException) as e:
                print('Could not click "Next page" button')

                self.driver.requests.clear()
                self.driver.refresh()
                time.sleep(1)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'has-chat-button')))
            
        

    def fetch_urls(self):

        print('Starting url fetcher')
        self.start_driver()
        first_hidden_api = self.first_api_fetch()
        second_hidden_api = self.second_api_fetch()
        return(first_hidden_api, second_hidden_api)
        self.driver.quit()


