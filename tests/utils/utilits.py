from ctypes.wintypes import tagSIZE

import requests
import asyncio
import aiohttp
from typing import Optional, Type, Union
from config import BaseConfig
from tests.utils.urls import DoctorsQueryBuilder, Ages


class NestedCard:
    _layer_fields: tuple
    _sub_layer_alias: Optional[str]
    _sub_layer_name: Optional[str]
    _sub_layer_obj: Optional[Type["NestedCard"]]

    def _set_fields_as_none(self):
        for field in self._layer_fields:
            setattr(self, field, None)

    def _fields_setting(self, data: dict):
        for field in self._layer_fields:
            if field in data.keys():
                setattr(self, field, data[field])
            else:
                setattr(self, field, None)

    def _layer_setting(self, data: dict):
        if self._sub_layer_obj and self._sub_layer_name and self._sub_layer_alias:
            if self._sub_layer_name in data.keys() and data[self._sub_layer_name]:
                slo = self._sub_layer_obj(data[self._sub_layer_name][0])
            else:
                slo = self._sub_layer_obj()
            setattr(self, self._sub_layer_alias, slo)

    def __init__(self, layer_data: Optional[dict] = None):
        if isinstance(layer_data, dict) and layer_data:
            self._fields_setting(layer_data)
            self._layer_setting(layer_data)
        else:
            self._set_fields_as_none()
            if self._sub_layer_obj and self._sub_layer_alias:
                setattr(self, self._sub_layer_alias, self._sub_layer_obj())


class Price(NestedCard):

    __slots__ = ('id', 'service_id')

    _layer_fields: tuple = ('id', 'service_id')
    _sub_layer_alias = None
    _sub_layer_name = None
    _sub_layer_obj = None

    def _fields_setting(self, data: dict):
        prices = data.get('prices', None)
        if isinstance(prices, list) and prices:
            for field in self._layer_fields:
                if field in prices[0]:
                    setattr(self, field, prices[0][field])
                else:
                    setattr(self, field, None)
        else:
            self._set_fields_as_none()


class Workplace(NestedCard):
    __slots__ = ('price', 'id', 'rta_id')

    _layer_fields: tuple = ('id', 'rta_id')
    _sub_layer_alias: str = 'price'
    _sub_layer_name: str = 'price_groups'
    _sub_layer_obj: Price = Price


class DoctorCard(NestedCard):
    __slots__ = ('workplace', 'id', 'code', 'name', 'rating')

    _layer_fields: tuple = ('id', 'code', 'name', 'rating')
    _sub_layer_alias: str = 'workplace'
    _sub_layer_name: str = 'workplaces'
    _sub_layer_obj: Workplace = Workplace


class DoctorCardDB:
    __slots__ = ('name', 'wid', 'did', 'service_id', 'rating', 'sign_sub_type', 'cpa_index', 'sort_rating_rate')

    def __init__(self, args):
        for pos, field in enumerate(self.__slots__):
            setattr(self, field, args[pos])


class DoctorListing:

    def __init__(self):
        self.doctor_cards: Union[list[DoctorCard], list[DoctorCardDB]] = []
        self.cards_workplaces: list[int] = []
        self.doc_ids: list[int] = []

    def add_card(self, card: Union[DoctorCard, DoctorCardDB]):
        self.doctor_cards.append(card)

        if isinstance(card, DoctorCard):
            self.doc_ids.append(card.id)

            if card.workplace.id:
                self.cards_workplaces.append(card.workplace.id)
        elif isinstance(card, DoctorCardDB):
            self.doc_ids.append(card.did)

            if card.wid:
                self.cards_workplaces.append(card.wid)

    def __eq__(self, other):
        wps_eq = self.cards_workplaces == other.cards_workplaces
        doc_eq = self.doc_ids == other.doc_ids
        return wps_eq and doc_eq


def parse_response_data(data: dict) -> Optional[DoctorListing]:
    listing_items: Optional[list] = data.get('items', None)
    if listing_items is None:
        return None

    doctors = DoctorListing()
    for item in listing_items:
        doctors.add_card(DoctorCard(item))

    return doctors


def get_response(url_query: dict[str: str], listing: str) -> requests.Response:
    url = "/".join((BaseConfig.base_url, listing))
    return requests.get(url, params=url_query)


class Case:
    spec: int
    serv: int
    page: int

    def __init__(self, spec, serv, page):
        self.spec = spec
        self.serv = serv
        self.page = page


async def fetch_single_url(session, url, spec, serv):
    try:
        async with session.get(url) as response:
            lp = await response.json()
            # step = int(lp['data']['last_page'] / 100 * 20)
            # return [Case(spec=spec, serv=serv, page=p) for p in list(range(1, lp['data']['last_page'], step))]
            return lp['data']['last_page']
    except Exception as e:
        # return f'Error fetching {url}: {e}'
        return None


async def fetch_data_async(cases_adult, cases_child):
    async with aiohttp.ClientSession() as session:
        tasks_adult = [fetch_single_url(session, c['url'], c['spec'], c['serv']) for c in cases_adult]
        tasks_child = [fetch_single_url(session, c['url'], c['spec'], c['serv']) for c in cases_child]
        result = await asyncio.gather(*tasks_adult, *tasks_child)
        return result[:len(cases_adult)], result[len(cases_adult):]


import time

def generate_parametrize(spec_serv, listing): # -> (list[Case], list[Case]):

    # t1 = time.time()

    cases: list[Case] = []
    cases_child: list[Case] = []

    base_url = "/".join((BaseConfig.base_url, listing))
    adult = []
    child = []

    for spec, serv, child_serv in zip(spec_serv['specialities'], spec_serv['services'], spec_serv['child_services']):
        if serv:
            url = base_url + DoctorsQueryBuilder(speciality_id=spec).get_query()
            adult.append({'url': url, 'spec': spec, 'serv': serv})
        if child_serv:
            url = base_url + DoctorsQueryBuilder(speciality_id=spec, age_type=Ages.child.value).get_query()
            child.append({'url': url, 'spec': spec, 'serv': child_serv})

    r_adult, r_child = asyncio.run(fetch_data_async(adult, child))

    for i, j in zip(adult, r_adult):
        step = int(j / 100 * 20)
        cases = cases + [Case(spec=i['spec'], serv=i['serv'], page=p) for p in list(range(1, j, step))]
    for i, j in zip(child, r_child):
        step = int(j / 100 * 20)
        cases_child = cases_child + [Case(spec=i['spec'], serv=i['serv'], page=p) for p in list(range(1, j, step))]

    # t2 = time.time()
    # diff = t2 - t1

    return cases, cases_child #, diff

    # t1 = time.time()
    #
    # cases: list[Case] = []
    # cases_child: list[Case] = []
    #
    # for spec, serv, c_serv in zip(spec_serv['specialities'], spec_serv['services'], spec_serv['child_services']):
    #     query = DoctorsQueryBuilder(speciality_id=spec)
    #     r = get_response(query.get_dict(), listing)
    #     if r.status_code == 200:
    #         r = r.json()
    #         lp = r['data'].get('last_page', None)
    #
    #         if lp > 0:
    #             step = int(lp/100*20)
    #             cases = cases + [Case(spec, serv, page) for page in list(range(1, lp, step))]
    #
    #     query = DoctorsQueryBuilder(speciality_id=spec, age_type=Ages.child.value)
    #     r = get_response(query.get_dict(), listing)
    #     if r.status_code == 200:
    #         r = r.json()
    #         lp = r['data'].get('last_page', None)
    #
    #         if lp > 0:
    #             step = int(lp/100*20)
    #             cases_child = cases_child + [Case(spec, c_serv, page) for page in list(range(1, lp, step))]
    #
    # t2 = time.time()
    # diff = t2 - t1
    #
    # return cases, cases_child, diff
