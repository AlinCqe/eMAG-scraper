import requests
import os
from requests.exceptions import JSONDecodeError
import time
import random
import pandas as pd
from bs4 import BeautifulSoup

from .db_config import collection

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,es;q=0.7,ro;q=0.6',
    'Referer': 'https://google.ro/',
    'DNT': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
}


fetch = []
items_id_used_set = set()

current_time = time.ctime(time.time())

def html_scraper(search_item):
    
    print('Starting HTML scraper')

    items_used_html_scraper = 0
    search_item_formated = search_item.strip().replace(' ', '+')
    response = requests.get(f'https://www.emag.ro/search/{search_item_formated}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.find_all('div', 'js-product-data')
    for item in items:

        item_id = int(item.get('data-product-id'))
        if item_id in items_id_used_set:
            continue
        
        item_name = item.get('data-name')
        item_price_and_currency = item.find('div', 'd-inline-flex align-items-center').find('p', 'product-new-price').text
        item_price_and_currency = item_price_and_currency.removeprefix('de la ')

        item_price, item_currency = item_price_and_currency.split(' ')


        collection.update_one(
            {'_id': item_id},
                {
                '$setOnInsert':{
                    'item_name': item_name
                },
                '$set':{
                    f'history.{current_time}': f'{item_price} {item_currency}'
                }
            }, 
            upsert=True)

        items_id_used_set.add(item_id)    
        items_used_html_scraper += 1


    print(f'Used a total of {items_used_html_scraper} items in the html scraper')
    print('HTML scraper finished')

def data_extract_first_api(first_hidden_api):
    items_used_count_first_api = 0
    print('Starting first api scraper')
    # Calls the first hidden api and saves items until there is no more data
    response = requests.get(first_hidden_api, headers=headers)
    data = response.json()
    items = data["data"]['adss']['product_collection']

    for item in items:
        # Check if item id hasnt been used
        item_id = int(item['id'])
        if item_id in items_id_used_set:
            continue

        item_name = item['name']
        item_price = item['offer']['price']['current']
        item_currency = item['offer']['price']['currency']['name']['display']
        
        collection.update_one(
            {'_id': item_id},
                {
                '$setOnInsert':{
                    'item_name': item_name
                },
                '$set':{
                    f'history.{current_time}': f'{item_price} {item_currency}'
                }
            }, 
            upsert=True)

        items_id_used_set.add(item_id)
        items_used_count_first_api += 1

    print(f'Used a total of {items_used_count_first_api} items with the first end point')
    print('First url scraper finished')


# Gets the second json file with more data and prints items + prices using second hidden url
def data_extract_second_api(second_hidden_api):
    items_used_count_second_api = 0
    # There may not be a second URL
    if second_hidden_api is None:
        return
    
    print('Starting second api scraper')
    page_number = 2
    try:
        while True:
            response = requests.get(second_hidden_api, headers=headers)
            data = response.json()
            items = data['data']['items']
            for item in items:
                item_id = int(item['id'])
                if item_id in items_id_used_set:
                    continue
                    
                item_name = item['name']
                item_price = item['offer']['price']['current']
                item_currency = item['offer']['price']['currency']['name']['display']
                
                items_id_used_set.add(item_id)
                items_used_count_second_api += 1


                collection.update_one(
                    {'_id': item_id},
                        {
                        '$setOnInsert':{
                            'item_name': item_name
                        },
                        '$set':{
                            f'history.{current_time}': f'{item_price} {item_currency}'
                        }
                    }, 
                    upsert=True)

            # Goes to the next page
            second_hidden_api = second_hidden_api.replace(fr'%2Fp{page_number}&', fr'%2Fp{page_number + 1}&')
            page_number += 1
            time.sleep(random.randint(1,5))
    # When the json file is corrupt finish
    except JSONDecodeError:
        print(f'Used a total of {items_used_count_second_api} items with the second end point')
        print('Second url scraper finished')



if __name__ == '__main__':
    data_extract_first_api()
    data_extract_second_api()
    html_scraper()