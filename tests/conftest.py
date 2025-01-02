import pytest
import psycopg2
from config import BaseConfig


# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope='module')
def db_con():
    db = psycopg2.connect(database=BaseConfig.db_conn['database'],
                          host=BaseConfig.db_conn['host'],
                          user=BaseConfig.db_conn['user'],
                          password=BaseConfig.db_conn['password'],
                          port=BaseConfig.db_conn['port'])
    cursor = db.cursor()
    yield cursor
    cursor.close()
    db.close()










