import pytest
from tests.utils import urls, utilits

# from urls import UrlParamsBuilder
# from utilits import fetch_data, parse_listing_data


specialities = [6480, 6457]
pages = [2, 4, 6]



# @pytest.mark.parametrize("get_items_by_request", request_parameters, indirect=True)
@pytest.mark.parametrize("spec", specialities)
@pytest.mark.parametrize("page", pages)
def test_base_doctor_sort(spec, page, db_get_data):
    url = urls.UrlParamsBuilder(page=page, speciality_id=spec)
    response = utilits.fetch_data(url)
    assert response.status_code == 200, f"Bad status code: {response.status_code}"

    response_data = response.json()
    response_data = response_data.get('data', None)
    assert response_data is not None, f"Empty response data"

    parsed_data = utilits.parse_listing_data(response_data)
    assert parsed_data is not None, f"No items in data"

    web_rta_ids = [card.rta_id for card in parsed_data]
    names = [card.workplace.id for card in parsed_data]
    data = db_get_data(web_rta_ids)

    web_equal_db = True
    for w_id, db_item in zip(names, data):
        if w_id != db_item[2]:
            web_equal_db = False
            break

    assert web_equal_db, "Web and DB not equal"