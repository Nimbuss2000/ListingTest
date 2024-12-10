import pytest
import requests
import psycopg2

from config import BaseConfig
from src import query_helper


# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope='module')
def db_con():
    db = psycopg2.connect(database=BaseConfig.db_conn['database'],
                          host=BaseConfig.db_conn['host'],
                          user=BaseConfig.db_conn['user'],
                          password=BaseConfig.db_conn['password'],
                          port=BaseConfig.db_conn['port'])
    cursor = db.cursor()
    yield  cursor
    cursor.close()
    db.close()


@pytest.fixture(scope='module')
def db_get_data(db_con):
    def get_request_data(items):
        s = "'" + "','".join(items) + "'"
        q = query_helper.query_doctors.format(s)
        db_con.execute(q)
        data = db_con.fetchall()
        db_cards = [query_helper.DoctorFromDb(row) for row in data]
        return db_cards
    yield get_request_data









