import requests
from bs4 import BeautifulSoup
import time
import json
from seleniumwire import webdriver
import random

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
driver = webdriver.Chrome()

driver.get(f'https://www.emag.ro/search/{search_item_formated}')


# Gets the hidden api where the data comes from
for request in driver.requests:
    if request.response:
        if request.url.startswith('https://sapi.emag.ro/recommendations/by-zone-by-filters'):
            hidden_api = f'{request.url}'
driver.quit()




offset_number = 0
for _ in range(20):
    # Changes the offset so we can iterate through all the pages
    previus_offset_number = offset_number if offset_number == 0 else offset_number - 12
    suffix = f'page%5Boffset%5D={previus_offset_number}&page%5Blimit%5D=12'
    hidden_api = hidden_api.replace(suffix, f'page%5Boffset%5D={offset_number}&page%5Blimit%5D=12')
    offset_number += 12

    # Calls the hidden api and prints data until there is no more data, raise a key error and exits the program
    response = requests.get(hidden_api, headers=headers)
    try:
        data = response.json()
        items = data["data"]['adss']['product_collection']
        for item in items:
            print(item['name'])
        time.sleep(random.randint(1,3))
    except KeyError:
        print('No more products')
        break   
    
