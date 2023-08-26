
def run():

    print("module: veld_registry")

    import psycopg2

    conn = psycopg2.connect(
        host="veldhub_db",
        database="ps_database",
        user="ps_user",
        password="ps_password"
    )

    print(conn)

    from veld_core.veld_core import VELD

    print(VELD.name)
