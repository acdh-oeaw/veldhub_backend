import psycopg2
from psycopg2 import OperationalError

from veld_core import settings
from veld_core.veld_dataclasses import Veld, VeldRepo


try:
    conn = psycopg2.connect(
        host=settings.db_host,
        database=settings.db_database,
        user=settings.db_user,
        password=settings.db_password,
    )
except OperationalError as ex:
    print(ex)
    conn = None


def register_veld_repo(veld_repo: VeldRepo) -> VeldRepo:
    for veld in veld_repo:
        veld = register_veld(veld)
    return veld_repo


def register_veld(veld: Veld) -> Veld:
    return veld


def get_veld_repos(**kwargs) -> VeldRepo:
    veld_repo = None
    return veld_repo
    
    
def get_velds(**kwargs) -> Veld:
    veld = None
    return veld


