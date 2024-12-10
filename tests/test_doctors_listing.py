from functools import lru_cache
from itertools import zip_longest
from tabulate import tabulate
import pytest
from tests.utils import urls
from tests.utils.utilits import fetch_data, parse_listing_data, DoctorCard

# from urls import UrlParamsBuilder
# from utilits import fetch_data, parse_listing_data


specialities = [6480, 6457]
pages = [13]



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

    parsed_data: list[DoctorCard] | None = parse_listing_data(response_data)
    assert parsed_data is not None, f"No items in data"

    rta_ids = [card.workplace.rta_id for card in parsed_data if card.workplace.rta_id is not None]
    db_data = db_get_data(rta_ids)

    compare_flag = True
    represent = {}
    for web_el, db_el in zip_longest(parsed_data, db_data):
        if web_el is None:
            compare_flag = False

        if db_el is None:
            compare_flag = False



        if web_el.name == db_el.doc_name:
            pass
        else:
            db
        web_doc_id = web_el.id
        try:
            db_doc_id = db_el[2]
        except TypeError:
            db_doc_id = None

        if web_doc_id != db_doc_id:
            compare_flag = False

        db_doc_id = db_el[1]
        represent.update({web_el.code: db_doc_id})

    assert compare_flag, print(tabulate(represent.items(), headers=["web", "db"], tablefmt="grid"))
