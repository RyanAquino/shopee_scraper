import psycopg2

DB_NAME = "shopee_scraper"
DB_PASS = "1"
DB_USER = "postgres"
DB_HOST = "localhost"


def verify_tables() -> bool:
    """
    Check if products table already exist
    :return: boolean if product table exist
    """
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    cur = conn.cursor()
    cur.execute(
        f"select exists(select * from information_schema.tables where table_name=%s)",
        ("products",),
    )
    exist = cur.fetchone()[0]
    conn.close()

    return exist


def create_product_table() -> None:
    """
    Create products table
    :return: None
    """
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(191), "
        "description VARCHAR(255), digital BOOLEAN default False, price FLOAT default 0, image VARCHAR, "
        "quantity INTEGER default 0, created_at timestamp default current_timestamp, UNIQUE (name))"
    )

    conn.commit()
    conn.close()
