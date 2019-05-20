import sqlite3
from sqlite3.dbapi2 import Error

DB_CREATE_TABLE = [
    """CREATE TABLE IF NOT EXISTS settings (
  setting text PRIMARY KEY,
  value text NOT NULL
)""",
    """CREATE TABLE IF NOT EXISTS roles (
  id integer PRIMARY KEY,
  name text UNIQUE NOT NULL,
  can_create_offers integer NOT NULL,
  can_manage_own_offers integer NOT NULL,
  can_manage_all_offers integer NOT NULL,
  can_listen_to_offers integer NOT NULL
)""",
    """CREATE TABLE IF NOT EXISTS users (
  id integer PRIMARY KEY,
  name text NOT NULL,
  phone text UNIQUE NOT NULL,
  role integer NOT NULL,
  FOREIGN KEY (role) REFERENCES roles (id)
)""",
    """CREATE TABLE IF NOT EXISTS seeds (
  id integer PRIMARY KEY,
  name text UNIQUE NOT NULL
)""",
    """CREATE TABLE IF NOT EXISTS offers (
  id integer PRIMARY KEY,
  poster integer NOT NULL,
  offer integer NOT NULL,
  request integer NOT NULL,
  recording text NOT NULL,
  timestamp text NOT NULL,
  FOREIGN KEY (poster) REFERENCES users (id),
  FOREIGN KEY (offer) REFERENCES seeds (id),
  FOREIGN KEY (request) REFERENCES seeds (id)
)"""
]

DB_SELECT_SETTING = """
SELECT value FROM settings WHERE settings.setting IS (?)
"""

DB_INSERT_SETTING = """
INSERT OR REPLACE INTO settings(setting, value) VALUES (?, ?)
"""

DB_SELECT_SEEDS = """
SELECT name FROM seeds
"""

DB_INSERT_SEED = """
INSERT INTO seeds(name) VALUES (?)
"""

DB_SELECT_USER = """
SELECT * FROM users WHERE phone IS (?)
"""

DB_SELECT_OFFERS_BY_USER = """
SELECT * FROM offers WHERE poster IS (?)
"""


def execute_query(conn, db_query, params=()):
    try:
        c = conn.cursor()
        c.execute(db_query, params)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
        return None


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(e)

    return None


def set_setting(conn, setting, value):
    try:
        c = conn.cursor()
        c.execute(DB_INSERT_SETTING, (setting, value))
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
        return value


def get_setting_or_default(conn, setting, value):
    try:
        c = conn.cursor()
        c.execute(DB_SELECT_SETTING, (setting,))
        result = c.fetchall()
        if len(result) < 1:
            set_setting(conn, setting, value)
            c.execute(DB_SELECT_SETTING, (setting,))
            result = c.fetchall()
        return result[0][0]
    except Error as e:
        print(e)
        return None


def get_all_seeds(conn):
    try:
        c = conn.cursor()
        c.execute(DB_SELECT_SEEDS)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
        return None


def add_seed(conn, name):
    try:
        c = conn.cursor()
        c.execute(DB_INSERT_SEED, (name,))
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
        return None


def select_user(conn, caller_id):
    try:
        c = conn.cursor()
        c.execute(DB_SELECT_USER, (caller_id,))
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
        return None


def select_offers(conn, user_id):
    try:
        c = conn.cursor()
        c.execute(DB_SELECT_OFFERS_BY_USER, (user_id,))
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
        return None
