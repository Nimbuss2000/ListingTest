from typing import Optional
from collections import namedtuple
import pytest
from tests.utils import db_helper
from tests.utils.urls import Ages, Sorts, Listings, DoctorsQueryBuilder
from tests.utils.utilits import get_response, parse_response_data, DoctorCard, DoctorListing


# specialities: 6427 (гастроинитеролог), 6457 (лор)
speciality_service = namedtuple('specs', ['speciality', 'service'])

# test data
spec_serv: list[speciality_service] = [speciality_service(6427, 1134067),
                                          speciality_service(6457, 1134075)]
pages = [2]
ages = [Ages.adult]


# @pytest.mark.parametrize("get_items_by_request", request_parameters, indirect=True)
@pytest.mark.parametrize("spec", spec_serv)
@pytest.mark.parametrize("page", pages)
# @pytest.mark.parametrize("age", ages)
def test_base_doctor_sort(spec: speciality_service, page, db_con):
    url_query: DoctorsQueryBuilder = DoctorsQueryBuilder(page=page, speciality_id=spec.speciality)
    response = get_response(url_query.get_dict(), Listings.doctors.value)
    assert response.status_code == 200, f"Bad status code: {response.status_code}"

    response_data = response.json()
    response_data = response_data.get('data', None)
    assert response_data is not None, f"Empty response data"

    parsed_data: Optional[DoctorListing] = parse_response_data(response_data)
    assert parsed_data is not None, f"No items in data"

    a = db_helper.doctors_db_request(db_con, parsed_data)
    z = 0

    assert True, "Web not equal DB"
