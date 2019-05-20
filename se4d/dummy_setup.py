from se4d import Database

DEFAULT_DB_FILE = "../db.sqlite"


def initialize():
    # Set up the database if it does not yet exist
    conn = Database.create_connection(DEFAULT_DB_FILE)
    for statement in Database.DB_CREATE_TABLE:
        print(Database.execute_query(conn, statement))
    #
    # Database.set_setting(conn, "host", "localhost")
    # Database.set_setting(conn, "port", "10123")
    # Database.set_setting(conn, "public_host", "vxml.valutadev.com")

    Database.add_seed(conn, "corn")
    Database.add_seed(conn, "rice")
    Database.add_seed(conn, "wheat")
    Database.add_seed(conn, "barley")
    Database.add_seed(conn, "sorghum")
    Database.add_seed(conn, "millet")

    conn.commit()

    seed_list = {"seed_list": [el[0] for el in Database.get_all_seeds(conn)]}
    print(seed_list)


initialize()
