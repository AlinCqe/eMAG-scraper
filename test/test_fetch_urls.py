from core.main import Driver
import pytest

search_item_mock = 'old spice'
search_item_mock_formated = 'old+spice'
first_hidden_api_mock = 'https://sapi.emag.ro/recommendations/by-zone-by-filters?source_id=7&zones=adss&identifier=0&filters%5Bquery%5D=vans&filters%5Bcategory%5D%5B%5D=2387&filters%5Bcategory%5D%5B%5D=2356&fields%5Bresized_images%5D=200x200%2C720x720&page%5Boffset%5D=0&page%5Blimit%5D=12'
second_hidden_api_mock = 'https://www.emag.ro/search-by-url?source_id=7&templates%5B%5D=full&url=%2Fsearch%2Fold%2Bspice%2Fp3&sort%5Bscore%5D=desc&listing_display_id=2&page%5Blimit%5D=60&page%5Boffset%5D=60&fields%5Bitems%5D%5Bimage_gallery%5D%5Bfashion%5D%5Blimit%5D=2&fields%5Bitems%5D%5Bimage%5D%5Bresized_images%5D=1&fields%5Bitems%5D%5Bresized_images%5D=200x200%2C350x350%2C720x720&fields%5Bitems%5D%5Bflags%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bbuying_options%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bflags%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bbundles%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bgifts%5D=1&fields%5Bitems%5D%5Bcharacteristics%5D=listing&fields%5Bquick_filters%5D=1&search_id=&search_fraze=&search_key='

class FakeRequest:
    def __init__(self, url, response):
        self.response = response
        self.url = url

list_fake_responses = [
    FakeRequest('https://example.com', True),
    FakeRequest(first_hidden_api_mock, True),
    FakeRequest('https://sapi.EMAG.com/ecommendations/by-zone-by-filters?source_id=7&zones=adss&identifier=0&filters%5Bquery%5D=vans&filters%5Bcategory%5D%5B%5D=2387&filters%5Bcategory%5D%5B%5D=2356&fields%5Bresized_images%5D=200x200%2C720x720&page%5Boffset%5D=0&page%5Blimit%5D=12', True),
    FakeRequest('https://ignored.com', None),
    FakeRequest('http://www.EMAG.ro/search-url?source_id=7&templates%5B%5D=full&url=%2Fsearch%2Fold%2Bspice%2Fp3&sort%5Bscore%5D=desc&listing_display_id=2&page%5Blimit%5D=60&page%5Boffset%5D=60&fields%5Bitems%5D%5Bimage_gallery%5D%5Bfashion%5D%5Blimit%5D=2&fields%5Bitems%5D%5Bimage%5D%5Bresized_images%5D=1&fields%5Bitems%5D%5Bresized_images%5D=200x200%2C350x350%2C720x720&fields%5Bitems%5D%5Bflags%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bbuying_options%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bflags%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bbundles%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bgifts%5D=1&fields%5Bitems%5D%5Bcharacteristics%5D=listing&fields%5Bquick_filters%5D=1&search_id=&search_fraze=&search_key=', True),
    FakeRequest(second_hidden_api_mock, True),
    FakeRequest("https://ignored.com", None)

]

driver = Driver(search_item_mock)

def test_search_item_foramt():
    assert driver.search_item_formated == search_item_mock_formated 



@pytest.mark.e2e
def test_first_url_gets_right_thing():

    first_api = driver.first_api_fetch()

    assert 'https://sapi.emag.ro/recommendations/by-zone-by-filters' in first_api
    assert isinstance(first_api, str)

def test_first_url_pagination_modify():
    assert driver.set_page_limit_to_100('page%5Boffset%5D=0&page%5Blimit%5D=10') == 'page%5Boffset%5D=0&page%5Blimit%5D=100'
    assert driver.set_page_limit_to_100('page%5Boffset%5D=0&page%5Blimit%5D=10&moreon=123') == 'page%5Boffset%5D=0&page%5Blimit%5D=100&moreon=123'


def test_url_catch():
    assert driver.get_url_from_requests(list_fake_responses, prefix='https://sapi.emag.ro/recommendations/by-zone-by-filters') == first_hidden_api_mock

    assert driver.get_url_from_requests(list_fake_responses, prefix='https://www.emag.ro/search-by-url?source_id=') == second_hidden_api_mock

@pytest.mark.e2e
def test_second_url_gets_right_thing():

    second_api = driver.second_api_fetch()
    
    assert isinstance(second_api, str)
    assert 'https://www.emag.ro/search-by-url?source_id=' in second_api


