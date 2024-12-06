import requests
from typing import Optional
from config import BaseConfig
from tests.utils.urls import UrlParamsBuilder
from pydantic import BaseModel, field_validator, Field


class Price(BaseModel):
    id: int
    service_id: int | None


class PricesGroup(BaseModel):
    discount: int
    price: Optional[Price] = Field(alias='prices')

    @field_validator("price", mode='before')
    def extract_first_price(cls, prices):
        if isinstance(prices, list) and prices:
            return prices[0]
        return None


class Workplace(BaseModel):
    id: int
    rta_id: str | None
    price_group: Optional[PricesGroup] = Field(alias="price_groups")

    @field_validator("price_group", mode='before')
    def extract_first_price_group(cls, price_groups):
        if isinstance(price_groups, list) and price_groups:
            return price_groups[0]
        return None


class DoctorCard(BaseModel):
    id: int
    code: str
    rating: float
    workplace: Optional[Workplace] = Field(alias="workplaces")

    @field_validator("workplace", mode='before')
    def extract_first_workplace(cls, workplaces):
        if isinstance(workplaces, list) and workplaces:
            return workplaces[0]
        return None

    def get_service(self) -> int | None:
        if self.workplace and self.workplace.price_group and self.workplace.price_group.price:
            return self.workplace.price_group.price.service_id
        else:
            return None

    def __getattr__(self, item):
        if item == 'rta_id':
            if self.workplace:
                return self.workplace.rta_id
            else:
                return None
        return super().__getattr__(item)


##########################################################

class WorkplaceV2:
    workplace_fields = ('id', 'rta_id')


    def _set_fields_as_none(self):
        for field in self.workplace_fields:
            self.__setattr__(field, None)

    def __init__(self, workplace: dict):
        if isinstance(workplace, dict):
            for field in self.workplace_fields:
                if field in workplace.keys():
                    self.__setattr__(field, workplace[field])
                else:
                    self.__setattr__(field, None)
            # if 'price_groups' in workplace.keys() and workplace['price_groups']:

        else:
            self._set_fields_as_none()


class DoctorCardV2:

    root_fields = ('id', 'code', 'name', 'rating')
    price_fields= ('id', 'service_id', 'price', 'title')

    def _set_fields_as_none(self):
        for field in self.root_fields:
            self.__setattr__(field, None)

    def __init__(self, card_data: dict):
        if isinstance(card_data, dict):
            for field in self.root_fields:
                if field in card_data.keys():
                    self.__setattr__(field, card_data[field])
                else:
                    self.__setattr__(field, None)
            if 'workplaces' in card_data.keys() and card_data['workplaces']:
                wp = WorkplaceV2(card_data['workplaces'][0])
                self.__setattr__('workplace', wp)
            else:
                self.__setattr__('workplace', None)
        else:
            self._set_fields_as_none()
            self.workplace = None

###########################################################


def parse_listing_data(data: dict):
    listing_items: list | None = data.get('items', None)
    if listing_items is None:
        return None

    a = DoctorCardV2(listing_items[0])
    aa = DoctorCardV2({})
    b = DoctorCardV2(['asd', 'dasd', 12312, None])
    c = DoctorCardV2({'asd': 1, 2123: 'asdas', 'www': 'www'})
    doctors: list[DoctorCard] = []
    for item in listing_items:
        doctors.append(DoctorCard.model_validate(item))
    return doctors


def fetch_data(url_params_obj: UrlParamsBuilder):
    payload = url_params_obj.get_query_params()
    url = "/".join((BaseConfig.base_url, url_params_obj.listing))
    r = requests.get(url, params=payload)
    return r



# class ListingDoctor:
#     doctor_id: int = None
#     code: str = None
#     name: str = None
#     rating: int = None
#     responses_count: int = None
#     scores_count: int = None
#     workplace: int = None
#     rtaId: str = None
#     clinic_id: int = None
#     service_id: int = None
#
#
# class ListingDoctors:
#     def get_doctors(self, request_json):
#         items = request_json['data']['items']
#         self.listing_doctors = {}
#         for count, item in enumerate(items):
#             doctor = ListingDoctor()
#             doctor.doctor_id = item['id']
#             doctor.code = item['code']
#             doctor.name = item['name']
#             doctor.rating = item['rating']
#             doctor.responses_count = item['responses_count']
#             doctor.scores_count = item['scores_count']
#             doctor.workplace = item['workplaces'][0]['id']
#             doctor.rtaId = item['workplaces'][0]['rta_id']
#             doctor.clinic_id = item['workplaces'][0]['clinic']['id']
#             doctor.service_id = item['workplaces'][0]['price_groups'][0]['prices'][0]['service_id']
#             self.listing_doctors[count] = doctor
#
#     def get_rta_ids(self):
#         return [self.listing_doctors[d].rtaId for d in self.listing_doctors]

