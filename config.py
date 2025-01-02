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


speciality_service = {
    'specialities':   [6427,    6457,    6480,    6478],
    'services':       [1134067, 1134064, 1134075, 1134082],
    'child_services': [1653436, 1653439, 1653428, 1653421]
}