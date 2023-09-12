import psycopg2
from veld_core.veld_dataclasses import Veld, VeldRepo


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


def _init_connection():
    conn = psycopg2.connect(
        host="veldhub_db",
        database="ps_database",
        user="ps_user",
        password="ps_password"
    )
    return conn
