import psycopg2
import os

DB_NAME = os.getenv("DB_NAME") or "shopee_scraper"
DB_PASS = os.getenv("DB_PASS") or "1"
DB_USER = os.getenv("DB_USER") or "postgres"
DB_HOST = os.getenv("DB_HOST") or "localhost"


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
def verify_tables(cur) -> bool:
    """
    Check if products table already exist
    :return: boolean if product table exist
    """
    cur.execute(
        f"select exists(select * from information_schema.tables where table_name=%s)",
        ("products",),
    )

    return cur.fetchone()[0]


@db_connection
def create_product_table(cur) -> None:
    """
    Create products table
    :return: None
    """
    cur.execute(
        "CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(191), "
        "description VARCHAR(10485760), digital BOOLEAN default False, price FLOAT default 0, image VARCHAR, "
        "quantity INTEGER default 0, created_at timestamp default current_timestamp)"
    )


@db_connection
def save_product(cur, data) -> None:
    """
    Save product details into the database
    :param cur: cursor
    :param data: Products model
    :return: None
    """
    cur.execute(
        "INSERT INTO products (name,description,price,image,quantity) "
        "VALUES(%(name)s, %(description)s, %(price)s, %(image)s, %(quantity)s)",
        data,
    )
