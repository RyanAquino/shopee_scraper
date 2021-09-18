import psycopg2
import os
from dotenv import load_dotenv, find_dotenv
import psycopg2.extensions

load_dotenv(find_dotenv())

DB_NAME = os.environ.get("DB_NAME") or "shopee_scraper"
DB_PASS = os.environ.get("DB_PASS") or "1"
DB_USER = os.environ.get("DB_USER") or "postgres"
DB_HOST = os.environ.get("DB_HOST") or "localhost"
DB_TABLE = os.environ.get("DB_TABLE") or "products_product"


def db_connection(func):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
        )
        cur = conn.cursor()
        value = func(cur, *args, **kwargs)
        conn.commit()
        conn.close()

        return value

    return wrapper


@db_connection
def verify_tables(cur: psycopg2.extensions.cursor) -> bool:
    """
    Check if products table already exist
    :return: boolean if product table exist
    """
    cur.execute(
        f"select exists(select * from information_schema.tables where table_name=%s)",
        (DB_TABLE,),
    )

    return cur.fetchone()[0]


@db_connection
def create_product_table(cur: psycopg2.extensions.cursor) -> None:
    """
    Create products table
    :return: None
    """
    cur.execute(
        f"CREATE TABLE {DB_TABLE} (id SERIAL PRIMARY KEY, name VARCHAR(10485760) UNIQUE, "
        "description VARCHAR(10485760), digital BOOLEAN default False, price FLOAT default 0, image VARCHAR, "
        "quantity INTEGER default 0, created_at timestamp default current_timestamp)"
    )


@db_connection
def save_product(cur: psycopg2.extensions.cursor, data: dict) -> None:
    """
    Save product details into the database
    :param cur: cursor
    :param data: Products model
    :return: None
    """
    cur.execute(
        f"INSERT INTO {DB_TABLE} (name,description,price,image_url,quantity,created_at) "
        "VALUES(%(name)s, %(description)s, %(price)s, %(image_url)s, %(quantity)s, %(created_at)s) "
        "ON CONFLICT (name) DO UPDATE SET (name, description, price, image, quantity, created_at) = "
        "(EXCLUDED.name, EXCLUDED.description, EXCLUDED.price, EXCLUDED.image_url, EXCLUDED.quantity,"
        "EXCLUDED.created_at)",
        data,
    )
