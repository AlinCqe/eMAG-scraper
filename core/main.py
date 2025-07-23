from .fetch_urls import Driver
from .data_scraper import DataScaper
from .query import get_items_by_ids
from concurrent.futures import ThreadPoolExecutor





class ScrapingSession:

    def __init__(self, search_item):

        self.search_item = search_item

        self.driver = Driver(self.search_item)
        self.data_scraper = DataScaper(self.search_item)

        self.first_hidden_api = None
        self.second_hidden_api = None


    def html_scraper(self):

        html_items_ids_used = self.data_scraper.html_scraper()

        return get_items_by_ids(ids_list=html_items_ids_used)


#make this wiht taht set_first api from the class after getting the urls from driver
    def first_api_scraper(self):

        self.first_hidden_api = self.driver.first_api_fetch()

        self.data_scraper.set_first_api(self.first_hidden_api)

        first_api_items_ids_used = self.data_scraper.data_extract_first_api()
        return get_items_by_ids(first_api_items_ids_used)

    def second_api_scraper(self):

        self.second_hidden_api = self.driver.second_api_fetch()

        if self.second_hidden_api:
            self.data_scraper.set_second_api(self.second_hidden_api)
            second_api_items_ids_used = self.data_scraper.data_extract_second_api()
            return get_items_by_ids(second_api_items_ids_used)
        

'''
def html_scraper(search_item):

    data_scraper = DataScaper(search_item, '', '')


    html_items_ids_used = data_scraper.html_scraper()

    return get_items_by_ids(ids_list=html_items_ids_used)



def first_api_scraper(search_item):

    driver = Driver(search_item=search_item)
    first_api = driver.first_api_fetch()

    data_scraper = DataScaper(search_item,first_api)
    first_api_items_ids_used = data_scraper.data_extract_first_api()

    return get_items_by_ids(first_api_items_ids_used)



    #First make endpoint with html page items, after continue with both endpoints(data_extract_first_api, data_extract_second_api functions)
   
    with ThreadPoolExecutor(max_workers=2) as executor:

        urls_future = executor.submit(driver.fetch_urls)

        html_first_future = executor.submit(html_scraper,search_item=search_item, search_item_words_list=search_item_words_list)
        html_items_id_used = html_first_future.result()
        
        html_second_future = executor.submit(get_items_by_ids,ids_list=html_items_id_used)
        html_items_data = html_second_future.result()
        
    
    first_hidden_api, second_hidden_api = urls_future.result()
    data_extract_first_api(first_hidden_api=first_hidden_api, search_item_words_list=search_item_words_list)
    if second_hidden_api:
        data_extract_second_api(second_hidden_api=second_hidden_api, search_item_words_list=search_item_words_list)
 


if __name__ == '__main__':
    html_scraper()

'''