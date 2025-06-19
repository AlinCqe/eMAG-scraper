import requests
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from requests.exceptions import JSONDecodeError
import pandas as pd
import os


options = Options()
options.add_argument('--headless')


search_item = str(input('What item do you want to search for? '))
search_item_formated = search_item.strip().replace(' ', '+')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,es;q=0.7,ro;q=0.6',
    'Referer': 'https://google.ro/',
    'DNT': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
}

driver = webdriver.Chrome(options=options)
driver.get(f'https://www.emag.ro/search/{search_item_formated}')
print(f'https://www.emag.ro/search/{search_item_formated}')


wait = WebDriverWait(driver, 10)


def get_first_hidden_api():
    first_hidden_api = None
    # Gets the first hidden api 
    while not first_hidden_api:
        for request in driver.requests:
            if request.response:
                if request.url.startswith('https://sapi.emag.ro/recommendations/by-zone-by-filters'):
                    first_hidden_api = f'{request.url}'
        driver.refresh()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'has-chat-button')))

    # Set the page items limit to max so we dont have to loop trought the same page
    suffix = f'page%5Boffset%5D=0&page%5Blimit%5D=12'
    first_hidden_api = first_hidden_api.replace(suffix, f'page%5Boffset%5D=0&page%5Blimit%5D=100')
    return first_hidden_api




# Gets the second hidden api that contains more data
def get_second_hidden_api():
    for _ in range(5):
        try:
            for request in driver.requests:
                if request.response.status_code == 200:
                    if request.url.startswith('https://www.emag.ro/search-by-url?source_id='):
                        second_hidden_api = f'{request.url}'
                        return second_hidden_api
                
            
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


first_hidden_api = get_first_hidden_api()
second_hidden_api = get_second_hidden_api()

driver.quit()



fetch = []
items_printed_count = 0

items_id_used_set = set()
def data_extract_first_api(api):
    global items_printed_count
    global fetch
    
    # Calls the first hidden api and prints data until there is no more data, raise a key error and exits the program
    response = requests.get(api, headers=headers)
    data = response.json()
    items = data["data"]['adss']['product_collection']
    for item in items:
        # Check if item id hasnt been used/printed
        if item['id'] in items_id_used_set:
            continue

        item_name = item['name']
        item_price = item['offer']['price']['current']
        item_currency = item['offer']['price']['currency']['name']['default']
        #print(item_name, item_currency, item_price)
        items_printed_count += 1

        fetch.append({'item_name': item_name, 'item_price': item_price, 'item_currency': item_currency})
        items_id_used_set.add(item['id'])
        
        if len(fetch) >= 200:
            df = pd.DataFrame(fetch) 
            df.to_csv('data.csv', mode='a', index=False, header=not os.path.exists('data.csv') )
            fetch = []



data_extract_first_api(first_hidden_api)

if second_hidden_api is not None:
# Gets the second json file with more data and prints items + prices using second hidden url
    page_number = 2
    try:
        while True:
            
            response = requests.get(second_hidden_api, headers=headers)
            data = response.json()
            items = data['data']['items']

            
            for item in items:

                if item['id'] in items_id_used_set:
                    continue
                items_id_used_set.add(item['id'])

                
                item_name = item['name']
                item_price = item['offer']['price']['current']
                item_currency = item['offer']['price']['currency']['name']['default']
                
                
                
                fetch.append({'item_name': item_name, 'item_price': item_price, 'item_currency': item_currency})
                items_printed_count += 1
                if len(fetch) >= 200:
                    df = pd.DataFrame(fetch) 
                    df.to_csv('data.csv', mode='a', index=False, header=not os.path.exists('data.csv') )
                    fetch = []


            # Goes to the next page
            second_hidden_api = second_hidden_api.replace(fr'%2Fp{page_number}&', fr'%2Fp{page_number + 1}&')

            page_number += 1
            time.sleep(random.randint(1,5))
       
    except JSONDecodeError:
        pass

df = pd.DataFrame(fetch) 
df.to_csv('data.csv', mode='a', index=False, header=not os.path.exists('data.csv') )
    
print(f'Script runned succsesfully with a total of {items_printed_count} items printed')















## FUNCIONA LO DE CATCH LAS URL, AHORA REQUEST ESAS URLS I RECOGER DATA DE ELLAS - done

# could change the while true loop and use insted of _ in range len(items in the jnson) as in the first url it should be just 100-done
# After that could change that repetitive thing of changing offset number - done 

# use a loop in the firts get hidden api, somethimes cant find tthe url i think,  it is not associated with a value - done

## UNA FUNCION, PARA LA PRIMERA URL DEBERIA FUNCIONAR, DE MIRAR SI FUNCTIONA CON LA SEGUNDA URL- DEPENDIENDO EN LA STRUCTURA DE JSON - done

# ultimo - la funcion de extract data funciona solo con el primer json, no con el segundo. toca hacer para el segundo - done
# puedo reciclar codigo, delete.txt, para recojer ese loop, ir cambiando paginas etc - done

# despues de hacer le funcion para la segunda api emepzar a guradar datos - done

# catch error, buscando g29 no tengo muchos items y no hay boton de next, cazar cuando da ese error posible mente con un simple try catchs - hecho creo/ revisar mas terde

# PROBLEMA !!! - hay item estaticos tmb, unos tmb con top favirtes que pueden venir de otra parte, no del endpoint
#puedo usar html scraper primero, y luego las dos hiddens api
#filtrar datos con id(lo que uso ahora)
#empezar a ordenar codigo ahora. es un poco messy






# crear nombre del archivo con el texto de la busceda, facil de hacer
# filtrar objetos que tengan el texto que he inputeado, a si no me da cremas cuando busca old spice
# talvez poder desactivar esto, preguntar un filtar si/no

# anadir lo de time para establecer cuando he encontrado este precio para poder comparar mas tarde


#Use logging or consistent prints to check the flow of execution.
'''
do prints like:
Got firts hidden api
got second hidden api
running data excart with firts api 
'''