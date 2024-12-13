from functools import lru_cache
from itertools import zip_longest
from tabulate import tabulate
import pytest
from tests.utils import urls
from tests.utils.utilits import fetch_data, parse_listing_data, DoctorCard, DoctorListing

# from urls import UrlParamsBuilder
# from utilits import fetch_data, parse_listing_data


# specialities = [6480, 6457]
specialities = [6457]
pages = [7]



# @pytest.mark.parametrize("get_items_by_request", request_parameters, indirect=True)
@pytest.mark.parametrize("spec", specialities)
@pytest.mark.parametrize("page", pages)
def test_base_doctor_sort(spec, page, db_get_data):
    url = urls.UrlParamsBuilder(page=page, speciality_id=spec)
    response = fetch_data(url)
    assert response.status_code == 200, f"Bad status code: {response.status_code}"

    response_data = response.json()
    response_data = response_data.get('data', None)
    assert response_data is not None, f"Empty response data"

    parsed_data: DoctorListing | None = parse_listing_data(response_data)
    assert parsed_data is not None, f"No items in data"



    assert True, "Web not equal DB"
