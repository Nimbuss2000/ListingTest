from itertools import repeat

from tests.utils.utilits import DoctorListing


class DoctorFromDb:

    __slots__ =  (
    'cli_name', 'doc_name', 'doc_id', 'workplace_id', 'service_id', 'sign_sub_type', 'cpa_index', 'sort_rating_rate')

    def __init__(self, data):
        for v, name in zip(data, self.__slots__):
            setattr(self, name, v)


query_doctors = '''
with wpInfo as (
    select workplace_id, doctor_id, clinic_id, service_id
    from rta.rta_workplaces
    where uuid in ({})
)
select c.name, d.name, d.id, wi.workplace_id, wi.service_id, wi.sign_sub_type, wci.cpa_index, dci.sort_rating_rate 
from wpInfo wpi
 join listing.workplace_indexes wi on wi.workplace_id = wpi.workplace_id
                                          and (wi.service_id = wpi.service_id
                                                   or (wi.service_id is NULL and wpi.service_id is NULL))
 join workplace_computed_infos wci on wci.workplace_id = wpi.workplace_id
 join doctors d on d.id = wpi.doctor_id
 join clinics c on c.id = wpi.clinic_id
 join doctor_computed_infos dci on dci.id = wpi.doctor_id
order by wi.sign_sub_type desc, wci.cpa_index desc, dci.sort_rating_rate desc
'''


class DoctorQueryGen:



    def __init__(self, data: DoctorListing, per_page: int = 20):
        if data.cards_workplaces:
            self.need_doctor_queries = True if len(data.cards_workplaces) < per_page else False
        else:
            self.need_doctor_queries = True
