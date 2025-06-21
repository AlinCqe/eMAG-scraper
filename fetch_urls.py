from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.service import Service
import time
import os

options = Options()
options.add_argument('--headless')
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
service = Service(log_path=os.devnull)
    


def fetch_urls(search_item):
    print('Starting url fetcher')
    driver = webdriver.Chrome(service=service,options=options)
    wait = WebDriverWait(driver, 10)

    search_item_formated = search_item.strip().replace(' ', '+')
    
    driver.get(f'https://www.emag.ro/search/{search_item_formated}')
    first_hidden_api = None


    # Gets the first hidden api 
    while not first_hidden_api:
        for request in driver.requests:
            if request.response:
                if request.url.startswith('https://sapi.emag.ro/recommendations/by-zone-by-filters'):
                    first_hidden_api = f'{request.url}'
                    print('Firts URL catched')
        driver.refresh()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'has-chat-button')))

    # Set the page items limit to max so we dont have to loop trought the same page
    suffix = f'page%5Boffset%5D=0&page%5Blimit%5D=12'
    first_hidden_api = first_hidden_api.replace(suffix, f'page%5Boffset%5D=0&page%5Blimit%5D=100')

    # Gets the second hidden api
    for _ in range(5):
        status = False
        try:
            for request in driver.requests:
                if request.response.status_code == 200:
                    if request.url.startswith('https://www.emag.ro/search-by-url?source_id='):
                        second_hidden_api = f'{request.url}'
                        print('Second URL catched')
                        status = True
                        break        
            if status == True:
                break                

            # Try clicking the cookies thing
            try:
                firts_cookies_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'btn.btn-primary.btn-block.js-accept.gtm_h76e8zjgoo')))
                firts_cookies_button.click()
            except (StaleElementReferenceException,TimeoutException):
                print('No "Close cookies pop-up" button was found')
                continue

            # Try closing the login thing
            try:
                close_loggin_notif_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'js-dismiss-login-notice-btn.dismiss-btn.btn.btn-link.py-0.px-0')))
                close_loggin_notif_button.click()
            except (StaleElementReferenceException, TimeoutException):
                print('No "Close login pop-up" button was found')
                continue

            # Try clicking next page button
            try:
                next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']")))
                next_page_button.click()
            except (StaleElementReferenceException, TimeoutException):
                print('No "Next" button was found')
                break

        # The request fetch/xhr url might be None, this catch the error, reload the page and continues
        except AttributeError:
            print('Couldnt find the seccond URL. Reload the page')
            driver.refresh()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'has-chat-button')))


    driver.quit()
    
    return first_hidden_api, second_hidden_api




if __name__ == '__main__':
    fetch_urls()
