from typing import Optional
from collections import namedtuple
import pytest
from tests.utils import db_helper
from tests.utils.urls import Ages, Sorts, Listings, DoctorsQueryBuilder
from tests.utils.utilits import get_response, parse_response_data, DoctorCard, DoctorListing


# specialities: 6427 (гастроинитеролог), 6457 (nevrol)
speciality_service = namedtuple('specs', ['speciality', 'service'])

# test data
spec_serv_adult: list[speciality_service] = [speciality_service(6427, 1134067), speciality_service(6457, 1134075)]
pages = [1, 10, 20, 45]


@pytest.mark.parametrize("spec", spec_serv_adult)
@pytest.mark.parametrize("page", pages)
def test_base_doctor_sort_adult(spec: speciality_service, page, db_con):
    url_query: DoctorsQueryBuilder = DoctorsQueryBuilder(page=page, speciality_id=spec.speciality)
    response = get_response(url_query.get_dict(), Listings.doctors.value)
    assert response.status_code == 200, f"Bad status code: {response.status_code}"

    response_data = response.json()
    response_data = response_data.get('data', None)
    assert response_data is not None, f"Empty response data"

    parsed_data: Optional[DoctorListing] = parse_response_data(response_data)
    assert parsed_data is not None, f"No items in data"

    cards_db: DoctorListing = db_helper.doctors_db_request(db_con, parsed_data, spec.service)
    eq = parsed_data == cards_db
    assert eq, f"DB not equal WEB"


spec_serv_child: list[speciality_service] = [speciality_service(6427, 1653436), speciality_service(6457, 1653439)]
pages_c = [1, 5, 10]


@pytest.mark.parametrize("spec", spec_serv_child)
@pytest.mark.parametrize("page", pages_c)
def test_base_doctor_sort_child(spec: speciality_service, page, db_con):
    url_query: DoctorsQueryBuilder = DoctorsQueryBuilder(page=page, speciality_id=spec.speciality, age_type=Ages.child)
    response = get_response(url_query.get_dict(), Listings.doctors.value)
    assert response.status_code == 200, f"Bad status code: {response.status_code}"

    response_data = response.json()
    response_data = response_data.get('data', None)
    assert response_data is not None, f"Empty response data"

    parsed_data: Optional[DoctorListing] = parse_response_data(response_data)
    assert parsed_data is not None, f"No items in data"

    cards_db: DoctorListing = db_helper.doctors_db_request(db_con, parsed_data, spec.service)
    eq = parsed_data == cards_db
    assert eq, f"DB not equal WEB"

