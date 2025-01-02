from enum import Enum
from pydantic import Field
from pydantic.dataclasses import dataclass


class Listings(Enum):
    doctors = 'doctors'
    clinics = 'clinics'

class Ages(Enum):
    adult = 'adult'
    child = 'child'

class Sorts(Enum):
    appointment = 'appointment'
    rating = 'rating'
    price = 'price'
    response = 'response'


@dataclass
class DoctorsQueryBuilder:
    """
    By default: ?city_code=spb
                &sort_by=appointment
                &with_meta=1
                &page=1
                &per_page=20
                &only_sign=0
                &only_high_rating=0
                &speciality_id=6480
                &age_type=adult
    """

    city_code: str = 'spb'
    sort_by: Sorts = Sorts.appointment
    with_meta: int = Field(ge=0, le=1, default=1)
    page: int = Field(ge=0, default=1)
    per_page: int =  Field(ge=1, le=50, default=20)
    only_sign: int = Field(ge=0, le=1, default=0)
    only_high_rating: int = Field(ge=0, le=1, default=0)
    speciality_id: int = 6480
    age_type: Ages = Ages.adult

    def get_query(self) -> str:
        params_list = []
        for param, value in self.__dict__.items():
            if issubclass(value.__class__, Enum):
                params_list.append(f'{param}={value.value}')
            else:
                params_list.append(f'{param}={value}')

        return '?'+'&'.join(params_list)


    def get_dict(self) -> dict[str: str]:
        payload = {}
        for param, value in self.__dict__.items():
            if issubclass(value.__class__, Enum):
                payload[param] = value.value
            else:
                payload[param] = value
        return payload