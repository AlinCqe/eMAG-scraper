import requests
from json import JSONDecodeError
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup

from .db_config import collection



class DataScraper:

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,es;q=0.7,ro;q=0.6',
            'Referer': 'https://google.ro/',
            'DNT': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
    }

    def __init__(self, search_item):

        self.search_item = search_item.lower()
        self.search_item_words = self.search_item.split()

        self.current_time = time.ctime(time.time())

        self.items_ids_skip_duplicates = set()

        self.html_items_ids_used = set()
        self.items_used_html_scraper = 0
        
        self.first_hidden_api = None
        self.first_api_items_ids_used = set()
        self.items_used_count_first_api = 0

        self.second_hidden_api = None
        self.second_api_items_ids_used = set()
        self.items_used_count_second_api = 0

        
    
    def set_first_api(self, first_hidden_api):
        self.first_hidden_api = first_hidden_api

    def set_second_api(self, second_hidden_api):
        self.second_hidden_api = second_hidden_api



    def html_scraper(self):

        """
        Scrapes data from eMAG html page based on the search item

        Filters item by name, avoids duplicates, and saves valid data to MongoDB
        Returns a list of the item IDs that were saved.
        """

        print('Starting HTML scraper')

        soup = self.fetch_html_data(search_item=self.search_item)
        items = soup.find_all('div', 'js-product-data')
    
        for item in items:
            item_data = self.parse_item_html(item)

            if item_data['item_id'] in self.items_ids_skip_duplicates:
                continue
            
            if not all(word in item_data['item_name'].lower() for word in self.search_item_words):
                continue

            item_data = {'item_id':item_data['item_id'],'item_name': item_data['item_name'], 'item_price':item_data['item_price'],'item_currency':item_data['item_currency']}
            
            if self.db_check_before_saving(item_data):
                self.db_saving(item_data)
        
            self.items_ids_skip_duplicates.add(item_data['item_id']) 
            self.html_items_ids_used.add(item_data['item_id']) 
            self.items_used_html_scraper += 1

        print(f'Used a total of {self.items_used_html_scraper} items in the html scraper')
        print('HTML scraper finished')
        return list(self.html_items_ids_used)
            

    def data_extract_first_api(self):

        """
        Scrapes product data from a first hidden API (up to ~100 items)

        Filters item by name, avoids duplicates, and saves valid data to MongoDB
        Returns a list of the item IDs that were saved.

        """

        items = self.fetch_api_data(self.first_hidden_api)['data']['adss']['product_collection']

        for item in items:

            try:
                item_data = self.parse_item_json(item)
 
            except KeyError:
                continue

            if item_data['item_id'] in self.items_ids_skip_duplicates:
                continue
            
            if not all(word in item_data['item_name'].lower() for word in self.search_item_words):
                continue

            if self.db_check_before_saving(item_data):
                self.db_saving(item_data)

            self.items_ids_skip_duplicates.add(item_data['item_id'])
            self.first_api_items_ids_used.add(item_data['item_id']) 
            self.items_used_count_first_api += 1


        print(f'Used a total of {self.items_used_count_first_api} items with the first end point')
        print('First url scraper finished')
        return list(self.first_api_items_ids_used)




    def data_extract_second_api(self):

        """
        Scrapes data from a second hidden API  (up to ~10,000 items, depending on the search item)

        Filters item by name, avoids duplicates, and saves valid data to MongoDB
        Returns a list of the item IDs that were saved.

        Warning: This method can take several minutes to complete.
        """

        if self.second_hidden_api is None:
            return None
        
        print('Starting second api scraper')
        page_number = 2

        while True:
            
            try:

                items = self.fetch_api_data(self.second_hidden_api)['data']['items']

            except JSONDecodeError:
                
                print(f'Used a total of {self.items_used_count_second_api} items with the second end point')
                print('Second url scraper finished')
                return list(self.second_api_items_ids_used)
                

            for item in items:

                try:
                    item_data = self.parse_item_json(item)

                except KeyError:
                    continue


                if item_data['item_id'] in self.items_ids_skip_duplicates:
                    continue

                if not all(word in item_data['item_name'].lower() for word in self.search_item_words):
                    continue

                if self.db_check_before_saving(item_data):
                    self.db_saving(item_data)
                
                self.items_ids_skip_duplicates.add(item_data['item_id'])
                self.items_used_count_second_api += 1
                self.second_api_items_ids_used.add(item_data['item_id']) 

            # Goes to the next page in the api
            self.second_hidden_api = self.second_hidden_api.replace(fr'%2Fp{page_number}&', fr'%2Fp{page_number + 1}&')
            page_number += 1
            time.sleep(random.randint(1,5))
            print('Going to the next page - second api scraper')




    def db_saving(self, item):

        """
        Saves item ID, name, price, and currency to MongoDB
        """

        collection.update_one(
            {'_id': item['item_id']},
                {
                '$setOnInsert':{
                    'item_name': item['item_name']
                },
                '$set':{
                    f'history.{self.current_time}': f'{item['item_price']} {item['item_currency']}'
                }
            }, 
            upsert=True)
        



    def db_check_before_saving(self, item):
        data = collection.find_one({'_id': item['item_id']})

        if not data:

            return True
        

        current_day = datetime.now().strftime("%a %b %d")
        history = data['history']
        date_match = None
        for day in history.keys():
            if current_day in day:
                date_match = day

        if date_match:

            if item['item_price'] == history[date_match].split()[0]:    
                return False
                



        '''

        items_saved_days = set()
        for day in history.keys():
            splitd = day.split()
            date_str = ' '.join(splitd[0:3])
            items_saved_days.add(date_str)


        if current_day in items_saved_days:
            if item['item_price'] == 


        '''


    def fetch_html_data(self, search_item):
        
        """
        Returns parsed html data 
        """

        search_item_formated = search_item.strip().replace(' ', '+')
        response = requests.get(f'https://www.emag.ro/search/{search_item_formated}', headers=self.headers)
        return BeautifulSoup(response.text, 'html.parser')


    def parse_item_html(self, item):

        """
        Parses item data from html
        Returns a dictionary with item ID, name, price, and currency
        """

        item_id = int(item.find('div', class_='card-v2') \
            .find('div', class_='card-v2-wrapper') \
            .find('div', class_='card-v2-toolbox') \
            .find('button', class_='card-compare-btn') \
            .get('data-prod-id').strip('"\''))   
        item_name = item.get('data-name')
        item_price_and_currency = item.find('div', 'd-inline-flex align-items-center').find('p', 'product-new-price').text
        item_price_and_currency = item_price_and_currency.removeprefix('de la ')
        item_price, item_currency = item_price_and_currency.split(' ')

        return {'item_id':item_id,'item_name': item_name, 'item_price':item_price,'item_currency':item_currency}




    def fetch_api_data(self, api):

        """
        Returns parsed API data 
        """

        response = requests.get(api, headers=self.headers)
        return response.json()
    

    def parse_item_json(self, item):

        """
        Parses item data from json format data
        Returns a dictionary with item ID, name, price, and currency
        """

        item_id = int(str(item['id']).strip('"\''))
        item_name = item['name']
        item_price = item['offer']['price']['current']
        item_currency = item['offer']['price']['currency']['name']['display']


        return {'item_id':item_id,'item_name': item_name, 'item_price':item_price,'item_currency':item_currency}
