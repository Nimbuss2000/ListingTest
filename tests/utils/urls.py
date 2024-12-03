# http://web-api.larionov.polygon.dev-napopravku.ru/api-internal/doctors/?city_code=spb&sort_by=appointment&with_meta=1&page=1&per_page=20&only_sign=0&only_high_rating=0&speciality_id=6480&age_type=adult
from copy import deepcopy

#todo добавить enum-ы как параметры объекта. + добавить pydentic

class UrlParamsBuilder:
    with_meta: int = 1
    per_page: int = 20
    only_sign: int = 0
    only_high_rating: int = 0

    listing: str
    city_code: str
    sort_by: str
    page: int
    speciality_id: int
    age_type: str

    def __init__(self,
                 listing:str="doctors",
                 city_code:str="spb",
                 sort_by:str="appointment",
                 page:int=1,
                 speciality_id:int=6480,
                 age_type:str="adult"):

        self.listing = listing
        self.city_code = city_code
        self.sort_by = sort_by
        self.page = page
        self.speciality_id = speciality_id
        self.age_type = age_type

    def get_query_params(self):
        req_params = {k: v for k, v in self.__dict__.items() if k != "listing"}
        opt_params = {k: v for k, v in self.__class__.__dict__.items() if not k.startswith('__') and not callable(v)}
        req_params.update(opt_params)
        return req_params

    def set_optional_params(self, **kwargs):
        for k, v in kwargs.items():
            try:
                self.k = v
            except Exception:
                print('Cant find param')
