"""
Author: Ryan Aquino
Description: Scrape shopee.com products per category and saves it to a Postgres database
"""
import concurrent.futures
from helpers.scrape_product_details_helper import (
    get_product_details,
    get_product_urls,
    driver,
)
from helpers.database import verify_tables, create_product_table, save_product
from loguru import logger


def scrape_task(url: str) -> list:
    """
    Scrape Job
    :param url: Product Category URL
    :return: List of product URL
    """
    chrome_driver = driver()
    products_urls = get_product_urls(chrome_driver, url)
    logger.info(f"Product Count: {len(products_urls)}")
    chrome_driver.close()

    return products_urls


def main() -> None:
    if not verify_tables():
        create_product_table()

    urls = [
        "https://shopee.ph/Cameras-cat.18560",
        "https://shopee.ph/Gaming-cat.20718",
        "https://shopee.ph/Laptops-Computers-cat.18596",
        "https://shopee.ph/Home-Entertainment-cat.18529",
        "https://shopee.ph/Mobiles-Gadgets-cat.24456",
        "https://shopee.ph/Men's-Shoes-cat.123",
        "https://shopee.ph/Mobile-Accessories-cat.109",
        "https://shopee.ph/Sports-Travel-cat.1029",
        "https://shopee.ph/Toys-Games-Collectibles-cat.115",
        "https://shopee.ph/Women's-Shoes-cat.531",
        "https://shopee.ph/Women's-Accessories-cat.106",
        "https://shopee.ph/Women's-Apparel-cat.102",
    ]
    product_list_urls = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(scrape_task, url) for url in urls]

        for process in concurrent.futures.as_completed(results):
            product_list_urls += process.result()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        product_details = [
            executor.submit(get_product_details, product_url)
            for product_url in product_list_urls
        ]

        for process in concurrent.futures.as_completed(product_details):
            try:
                logger.info(f"{process.result()['name']} - Processing")
                save_product(process.result())
                logger.info(f"{process.result()['name']} - Success")
            except Exception as e:
                logger.exception(f"Exception: {str(e)}")


if __name__ == "__main__":
    main()
