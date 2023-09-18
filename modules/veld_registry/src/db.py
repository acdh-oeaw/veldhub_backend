import pymongo

from veld_core import settings


try:
    client = pymongo.MongoClient(
        f"mongodb://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}"
    )
    db = client[settings.db_database]
except Exception as ex:
    print(ex)
    db = None
