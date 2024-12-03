import psycopg2
from config import BaseConfig


class DB:
    __connection = None
    __cursor = None

    def __init__(self):
        self.__connection = psycopg2.connect(database=BaseConfig.db_conn['database'],
                                           host=BaseConfig.db_conn['host'],
                                           user=BaseConfig.db_conn['user'],
                                           password=BaseConfig.db_conn['password'],
                                           port=BaseConfig.db_conn['port'])

    def get_cursor(self):
        if self.__cursor:
            return self.__cursor
        self.__cursor = self.__connection.cursor()

    