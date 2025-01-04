from typing import Optional
from collections import namedtuple
import pytest
import config
from tests.utils import db_helper
from tests.utils.urls import Ages, Listings, DoctorsQueryBuilder
from tests.utils.utilits import get_response, parse_response_data, DoctorListing, generate_parametrize, Case


class TestDoctors:

    # cases, cases_child = generate_parametrize(config.speciality_service, Listings.doctors.value)
    adult_cases, child_cases = generate_parametrize(config.speciality_service, Listings.doctors.value)


    @pytest.mark.parametrize("case", adult_cases)
    def test_base_doctor_sort_adult(self, case: Case, db_con):
        url_query: DoctorsQueryBuilder = DoctorsQueryBuilder(page=case.page, speciality_id=case.spec)
        response = get_response(url_query.get_dict(), Listings.doctors.value)
        assert response.status_code == 200, f"Bad status code: {response.status_code}"

        response_data = response.json()
        response_data = response_data.get('data', None)
        assert response_data is not None, f"Empty response data"

        parsed_data: Optional[DoctorListing] = parse_response_data(response_data)
        assert parsed_data is not None, f"No items in data"

        cards_db: DoctorListing = db_helper.doctors_db_request(db_con, parsed_data, case.serv)
        eq = parsed_data == cards_db
        # print(f"Spec: {case.spec}, Serv: {case.serv}, Page: {case.page}")
        assert eq, f"DB not equal WEB"


    @pytest.mark.parametrize("case", child_cases)
    def test_base_doctor_sort_child(self, case: Case, db_con):
        url_query: DoctorsQueryBuilder = DoctorsQueryBuilder(page=case.page, speciality_id=case.spec, age_type=Ages.child)
        response = get_response(url_query.get_dict(), Listings.doctors.value)
        assert response.status_code == 200, f"Bad status code: {response.status_code}"

        response_data = response.json()
        response_data = response_data.get('data', None)
        assert response_data is not None, f"Empty response data"

        parsed_data: Optional[DoctorListing] = parse_response_data(response_data)
        assert parsed_data is not None, f"No items in data"

        cards_db: DoctorListing = db_helper.doctors_db_request(db_con, parsed_data, case.serv)
        eq = parsed_data == cards_db
        # print(f"Spec: {case.spec}, Serv: {case.serv}, Page: {case.page}")
        assert eq, f"DB not equal WEB"

