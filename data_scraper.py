import requests
import os
from requests.exceptions import JSONDecodeError
import time
import random
import pandas as pd
from bs4 import BeautifulSoup

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

def html_scraper(search_item):

    print('Starting HTML scraper')

    itmes_used_html_scraper = 0
    search_item_formated = search_item.strip().replace(' ', '+')
    response = requests.get(f'https://www.emag.ro/search/{search_item_formated}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    itmes = soup.find_all('div', 'js-product-data')
    for item in itmes:
        if item.get('data-product-id') in items_id_used_set:
            continue

        item_name = item.get('data-name')
        item_price_and_currency = item.find('div', 'd-inline-flex align-items-center').find('p', 'product-new-price').text
        item_price, item_currency = item_price_and_currency.split(' ')

        fetch.append({'item_name': item_name, 'item_price': item_price, 'item_currency': item_currency})
        items_id_used_set.add(item.get('data-product-id'))    
        itmes_used_html_scraper += 1

    df = pd.DataFrame(fetch) 
    df.to_csv('data.csv', mode='a', index=False)
    fetch.clear()

    print(f'Used a total of {itmes_used_html_scraper} items')
    print('HTML scraper finished')


def data_extract_first_api(first_hidden_api):
    items_used_count_first_api = 0
    print('Starting first api scraper')
    # Calls the first hidden api and prints data until there is no more data, raise a key error and exits the program
    response = requests.get(first_hidden_api, headers=headers)
    data = response.json()
    items = data["data"]['adss']['product_collection']
    for item in items:
        # Check if item id hasnt been used/printed
        if item['id'] in items_id_used_set:
            continue

        item_name = item['name']
        item_price = item['offer']['price']['current']
        item_currency = item['offer']['price']['currency']['name']['display']
        
        fetch.append({'item_name': item_name, 'item_price': item_price, 'item_currency': item_currency})
        items_id_used_set.add(item['id'])
        items_used_count_first_api += 1

    if len(fetch) >= 200:
        df = pd.DataFrame(fetch) 
        df.to_csv('data.csv', mode='a', index=False)
        fetch.clear()

    

    df = pd.DataFrame(fetch) 
    df.to_csv('data.csv', mode='a', index=False)
    
    print(f'Total items printed with the first url: {items_used_count_first_api}')
    print('First url scraper finished')

# Gets the second json file with more data and prints items + prices using second hidden url
def data_extract_second_api(second_hidden_api):
    items_used_count_second_api = 0
    # There may not be a second URL
    if second_hidden_api is not None:
        print('Starting second api scraper')
        page_number = 2
        try:
            while True:
                
                response = requests.get(second_hidden_api, headers=headers)
                data = response.json()

                items = data['data']['items']
                for item in items:

                    if item['id'] in items_id_used_set:
                        continue
                    
                    item_name = item['name']
                    item_price = item['offer']['price']['current']
                    item_currency = item['offer']['price']['currency']['name']['display']
                    
                    fetch.append({'item_name': item_name, 'item_price': item_price, 'item_currency': item_currency})
                    items_id_used_set.add(item['id'])
                    items_used_count_second_api += 1

                if len(fetch) >= 200:
                    df = pd.DataFrame(fetch) 
                    df.to_csv('data.csv', mode='a', index=False)
                    fetch.clear()


                # Goes to the next page
                second_hidden_api = second_hidden_api.replace(fr'%2Fp{page_number}&', fr'%2Fp{page_number + 1}&')
                page_number += 1
                time.sleep(random.randint(1,5))
        # When the json file is corrupt finish
        except JSONDecodeError:
            
            df = pd.DataFrame(fetch) 
            df.to_csv('data.csv', mode='a', index=False, header=not os.path.exists('data.csv') )

            print(f'Total items printed from the second url: {items_used_count_second_api}')
            print('Second url scraper finished')



# Stores the items that my be left in memory
df = pd.DataFrame(fetch) 
df.to_csv('data.csv', mode='a', index=False)

# header=not os.path.exists('data.csv')


if __name__ == '__main__':
    data_extract_first_api()
    data_extract_second_api()
    html_scraper()