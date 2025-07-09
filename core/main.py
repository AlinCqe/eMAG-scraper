from .fetch_urls import Driver
from .data_scraper import data_extract_first_api, data_extract_second_api, html_scraper
from .query import get_items_by_ids
from concurrent.futures import ThreadPoolExecutor


def main(search_item):
    
    #driver = Driver(search_item=search_item)
    search_item_words_list = search_item.split() 

    html_items_id_used = html_scraper(search_item=search_item,search_item_words_list=search_item_words_list)

    html_items_data = get_items_by_ids(ids_list=html_items_id_used)

    return get_items_by_ids(ids_list=html_items_id_used)


    #First make endpoint with html page items, after continue with both endpoints(data_extract_first_api, data_extract_second_api functions)
    '''
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
    '''


if __name__ == '__main__':
    main()

