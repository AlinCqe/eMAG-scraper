from .fetch_urls import Driver
from .data_scraper import data_extract_first_api, data_extract_second_api, html_scraper


def main(search_item):

    driver = Driver(search_item=search_item)

    first_hidden_api, second_hidden_api = driver.fetch_urls()
    print(first_hidden_api, second_hidden_api)

    search_item_words_list = search_item.split()   

    html_scraper(search_item=search_item, search_item_words_list=search_item_words_list)
    data_extract_first_api(first_hidden_api=first_hidden_api, search_item_words_list=search_item_words_list)

    if second_hidden_api:
        data_extract_second_api(second_hidden_api=second_hidden_api, search_item_words_list=search_item_words_list)

if __name__ == '__main__':
    main()

