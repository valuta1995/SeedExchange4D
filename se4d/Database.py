import sqlite3
from sqlite3.dbapi2 import Error

DB_CREATE_TABLE = [
    """CREATE TABLE IF NOT EXISTS settings (
  setting text PRIMARY KEY,
  value text NOT NULL
)""",
    """CREATE TABLE IF NOT EXISTS roles (
  id integer PRIMARY KEY,
  name text UNIQUE NOT NULL
)""",
    """CREATE TABLE IF NOT EXISTS users (
  id integer PRIMARY KEY,
  name text NOT NULL,
  phone text NOT NULL,
  role integer NOT NULL,
  FOREIGN KEY (role) REFERENCES roles (id)
)""",
    """CREATE TABLE IF NOT EXISTS seeds (
  id integer PRIMARY KEY,
  name text NOT NULL
)""",
    """CREATE TABLE IF NOT EXISTS offers (
  id integer PRIMARY KEY,
  offer integer,
  request integer,
  timestamp text,
  FOREIGN KEY (offer) REFERENCES seeds (id),
  FOREIGN KEY (request) REFERENCES seeds (id)
)"""
]

DB_SELECT_SETTING = """
SELECT value FROM settings WHERE settings.setting IS ?
"""

DB_INSERT_SETTING = """
INSERT INTO settings(setting, value) VALUES (?, ?)
"""

DB_SELECT_SEEDS = """
SELECT name FROM seeds
"""

BG_SELECT_KEYWORDS = """
SELECT * FROM keywords
"""

BG_SELECT_KEYWORDS_BY_NAME = """
SELECT * FROM keywords WHERE keywords.name LIKE ?
"""

BG_SELECT_CITIES = """
SELECT * FROM cities WHERE cities.id IN (
  SELECT city_id from keywords_cities WHERE keywords_cities.keyword_id IS ?
)"""

BG_SELECT_SENTIMENT = """
SELECT *
FROM sentiments
WHERE sentiments.id IN (
  SELECT tweets.id
  FROM tweets
  WHERE tweets.keyword_city_id IN (
    SELECT keywords_cities.id
    FROM keywords_cities
    WHERE keywords_cities.keyword_id IS ?
      AND keywords_cities.city_id IS ?
  )
)"""

BG_INSERT_KEYWORDS = """
INSERT INTO keywords(enabled, name, twitter_query, keyword_regex, cities_list, min_tweet_count, max_tweet_count)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""

BG_INSERT_KEYWORDS_CITIES = """
INSERT INTO keywords_cities(keyword_id, city_id, cluster) VALUES (?, ?, ?) 
"""

BG_SELECT_CITIES_COLLECTION = """
SELECT * FROM cities WHERE cities.id IN (
    SELECT cities_collection.city_id FROM cities_collection WHERE cities_collection.name LIKE ?
)"""

BG_SELECT_COLLECTION_NAME = """
SELECT name FROM cities_collection WHERE cities_collection.id IS ?
"""

BG_SELECT_COLLECTION_ID = """
SELECT id FROM cities_collection WHERE cities_collection.name LIKE ?
"""

BG_SELECT_TWEETS = """
SELECT * FROM tweets WHERE tweets.keyword_city_id IN (
  SELECT keywords_cities.id FROM keywords_cities WHERE 
    keywords_cities.keyword_id IS ? AND
    keywords_cities.city_id IS ? 
)
"""

BG_INSERT_TWEET = """
INSERT OR IGNORE INTO tweets(id, body, time, keyword_city_id) VALUES (?, ?, ?, ?) 
"""

BG_INSERT_SENTIMENT = """
INSERT INTO sentiments(id, score, sentiment) VALUES (?, ?, ?) 
"""


def set_setting(conn, setting, value):
    try:
        c = conn.cursor()
        c.execute(DB_INSERT_SETTING, setting, value)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
        return value


def get_setting_or_default(conn, setting, value):
    try:
        c = conn.cursor()
        c.execute(DB_SELECT_SETTING, setting)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
        set_setting(conn, setting, value)
        try:
            c = conn.cursor()
            c.execute(DB_SELECT_SETTING, setting)
            result = c.fetchall()
            return result
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
        return conn
    except Error as e:
        print(e)

    return None