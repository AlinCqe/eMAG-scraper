import requests
from requests.exceptions import JSONDecodeError
import time
import random
from bs4 import BeautifulSoup

from .db_config import collection



class DataScaper:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,es;q=0.7,ro;q=0.6',
        'Referer': 'https://google.ro/',
        'DNT': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

    def __init__(self, search_item, first_hidden_api, second_hidden_api):

        self.search_item = search_item.lower()
        self.search_item_words = self.search_item.split()

        self.current_time = time.ctime(time.time())

        self.items_ids_skip_duplicates = set()

        self.html_items_ids_used = set()
        self.items_used_html_scraper = 0
        
        self.first_hidden_api = first_hidden_api
        self.first_api_items_ids_used = set()
        self.items_used_count_first_api = 0

        self.second_hidden_api = second_hidden_api
        self.second_api_items_ids_used = set()
        self.items_used_count_second_api = 0

        
    def html_scraper(self):
        
        print('Starting HTML scraper')

        search_item_formated = self.search_item.strip().replace(' ', '+')
        response = requests.get(f'https://www.emag.ro/search/{search_item_formated}', headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.find_all('div', 'js-product-data')
        for item in items:

            item_id = int(item.get('data-product-id'))
            item_name = item.get('data-name')
            item_price_and_currency = item.find('div', 'd-inline-flex align-items-center').find('p', 'product-new-price').text
            item_price_and_currency = item_price_and_currency.removeprefix('de la ')
            item_price, item_currency = item_price_and_currency.split(' ')


            if item_id in self.items_ids_skip_duplicates:
                continue
            
            if not all(word in item_name.lower() for word in self.search_item_words):
                continue

            


            collection.update_one(
                {'_id': item_id},
                    {
                    '$setOnInsert':{
                        'item_name': item_name
                    },
                    '$set':{
                        f'history.{self.current_time}': f'{item_price} {item_currency}'
                    }
                }, 
                upsert=True)

            self.items_ids_skip_duplicates.add(item_id) 
            self.html_items_ids_used.add(item_id) 
            self.items_used_html_scraper += 1
            print(item_name, item_price, item_currency)

        print(f'Used a total of {self.items_used_html_scraper} items in the html scraper')
        print('HTML scraper finished')
        return list(self.html_items_ids_used)
            


    def data_extract_first_api(self):

        print('Starting first api scraper')
        # Calls the first hidden api and saves items until there is no more data
        response = requests.get(self.first_hidden_api, headers=self.headers)
        data = response.json()
        items = data["data"]['adss']['product_collection']

        for item in items:
            
            item_id = int(item['id'])
            item_name = item['name']
            item_price = item['offer']['price']['current']
            item_currency = item['offer']['price']['currency']['name']['display']

            # Check if item id hasnt been used
            if item_id in self.items_ids_skip_duplicates:
                continue
            
            if not all(word in item_name.lower() for word in self.search_item_words):
                continue

            
            collection.update_one(
                {'_id': item_id},
                    {
                    '$setOnInsert':{
                        'item_name': item_name
                    },
                    '$set':{
                        f'history.{self.current_time}': f'{item_price} {item_currency}'
                    }
                }, 
                upsert=True)

            self.items_ids_skip_duplicates.add(item_id)
            self.first_api_items_ids_used.add(item_id) 
            self.items_used_count_first_api += 1
            print(item_name,item_price,item_currency)

        print(f'Used a total of {self.items_used_count_first_api} items with the first end point')
        print('First url scraper finished')



    def data_extract_second_api(self):
        # There may not be a second URL
        if self.second_hidden_api is None:
            return
        
        print('Starting second api scraper')
        page_number = 2

        while True:
            
            try:
                response = requests.get(self.second_hidden_api, headers=self.headers)
                data = response.json()
                items = data['data']['items']
            except JSONDecodeError:
                print(f'Used a total of {self.items_used_count_second_api} items with the second end point')
                print('Second url scraper finished')
                break

            for item in items:

                try:
                    item_id = int(item['id'])
                    item_name = item['name']
                    item_price = item['offer']['price']['current']
                    item_currency = item['offer']['price']['currency']['name']['display']
                except KeyError:
                    continue

                if item_id in self.items_ids_skip_duplicates:
                    continue

                if not all(word in item_name.lower() for word in self.search_item_words):
                    continue

                collection.update_one(
                    {'_id': item_id},
                        {
                        '$setOnInsert':{
                            'item_name': item_name
                        },
                        '$set':{
                            f'history.{self.current_time}': f'{item_price} {item_currency}'
                        }
                    }, 
                    upsert=True)
                
                self.items_ids_skip_duplicates.add(item_id)
                self.items_used_count_second_api += 1
                self.second_api_items_ids_used.add(item_id) 

            # Goes to the next page
            self.second_hidden_api = self.second_hidden_api.replace(fr'%2Fp{page_number}&', fr'%2Fp{page_number + 1}&')
            page_number += 1
            time.sleep(random.randint(1,5))
