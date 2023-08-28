import psycopg2
from veld_core.dataclasses import VELD


def init_connection():
    conn = psycopg2.connect(
        host="veldhub_db",
        database="ps_database",
        user="ps_user",
        password="ps_password"
    )
    print(conn)
    

    print(VELD.name)
