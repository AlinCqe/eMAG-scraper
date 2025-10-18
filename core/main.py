from .fetch_urls import Driver
from .data_scraper import DataScraper
from .query import get_items_by_ids
from concurrent.futures import ThreadPoolExecutor





class ScrapingSession:

    def __init__(self, search_item):

        self.search_item = search_item

        self.driver = Driver(self.search_item)
        self.data_scraper = DataScraper(self.search_item)

        self.first_hidden_api = None
        self.second_hidden_api = None

    def html_scraper(self):

        html_items_ids_used = self.data_scraper.html_scraper()

        return get_items_by_ids(ids_list=html_items_ids_used)

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
        

        return []


def main():



    session = ScrapingSession("old spice deodorant stick")
    
    session.html_scraper()
    session.first_api_scraper()
    session.second_api_scraper()
    
if __name__ =="__main__":
    main()