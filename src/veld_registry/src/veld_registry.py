import psycopg2
from veld_core.dataclasses import Veld, VeldRepo


def insert_veld_repo(veld_repo: VeldRepo):
    pass


def update_veld_repo(veld_repo: VeldRepo):
    pass


def get_veld_repo() -> VeldRepo:
    pass


def get_veld() -> Veld:
    pass


def _init_connection():
    conn = psycopg2.connect(
        host="veldhub_db",
        database="ps_database",
        user="ps_user",
        password="ps_password"
    )
    return conn
