from psycopg2.extensions import cursor
from tests.utils.utilits import DoctorListing


# Запрос за врачами, если с веба у всех карточек есть воркплейсы
query_doctors_only_workplaces = '''
with base_collector as (
select d.name, w.id wid, d.id did, wi.service_id, dci.rating, wi.sign_sub_type, wci.cpa_index, dci.sort_rating_rate from workplaces w
 left join listing.workplace_indexes wi on wi.workplace_id = w.id
 join workplace_computed_infos wci on wci.workplace_id = w.id 
 join doctors d on d.id = w.doctor_id 
 left join doctor_computed_infos dci on dci.id = w.doctor_id
where w.id in ({})
and (wi.service_id is null or wi.service_id = {})
)
select * from base_collector bc
where not (
	bc.service_id is null
	and exists (
		select 1 
		from base_collector temp_bc 
		where temp_bc.wid = bc.wid 
		and temp_bc.service_id is not null 
	)
)
order by bc.sign_sub_type desc, bc.cpa_index desc nulls last, bc.sort_rating_rate desc nulls last, bc.did asc
'''

# Запрос за врачами, если с веба не у всех карточек есть воркплейсы
query_doctors_workplaces_and_ids = '''
with base_collector as (
select w.id wid, d.id did, wi.service_id, dci.rating, wi.sign_sub_type, wci.cpa_index, dci.sort_rating_rate from workplaces w
 left join listing.workplace_indexes wi on wi.workplace_id = w.id
 join workplace_computed_infos wci on wci.workplace_id = w.id 
 join doctors d on d.id = w.doctor_id 
 left join doctor_computed_infos dci on dci.id = w.doctor_id
where w.id in ({}})
and (wi.service_id is null or wi.service_id = {})
)
select d.name, bc.wid, dci.id did, bc.service_id, dci.rating, bc.sign_sub_type, bc.cpa_index, dci.sort_rating_rate from doctor_computed_infos dci
	join doctors d on d.id = dci.id
	left join base_collector bc on bc.did = dci.id 
where dci.id in ({})
order by bc.sign_sub_type desc nulls last, bc.cpa_index desc nulls last, dci.sort_rating_rate desc nulls last, dci.id asc
'''


def doctors_db_request(db: cursor, data: DoctorListing, per_page: int = 20):

    s = ""
    return 23
