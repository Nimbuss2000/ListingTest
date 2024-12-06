from db_pass import DB_PASS

class BaseConfig:
    base_url = "http://web-api.larionov.polygon.dev-napopravku.ru/api-internal"
    db_conn = {
        "database": "napopravku",
        "host": "test-base-2.np-internal.ru",
        "user": "napopravku",
        "password": DB_PASS,
        "port": "5024"
    }
