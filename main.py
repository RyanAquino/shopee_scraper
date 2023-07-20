"""
Author: Ryan Aquino
Description: Scrape shopee.com products per category and saves it to a Postgres database
"""
import concurrent.futures
from datetime import datetime

from loguru import logger

from helpers.database import create_product_table, save_product, verify_tables
from helpers.scrape_product_details_helper import (
    driver,
    get_product_details,
    get_product_urls,
)


def scrape_task(url: str) -> list:
    """
    Scrape Job
    :param url: Product Category URL
    :return: List of product URL
    """
    chrome_driver = driver()
    products_urls = get_product_urls(chrome_driver, url)
    logger.info(f"Product Count: {len(products_urls)}")
    chrome_driver.quit()

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
    exception_urls = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = [executor.submit(scrape_task, url) for url in urls]

        for process in concurrent.futures.as_completed(results):
            product_list_urls += process.result()

    products_count = len(product_list_urls)
    logger.info(products_count)

    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        product_details = [
            executor.submit(get_product_details, product_url)
            for product_url in product_list_urls
        ]

        for process in concurrent.futures.as_completed(product_details):
            try:
                result = process.result()
                if not result:
                    continue

                print(result)
                logger.info(f"{result['name']} - Processing")
                save_product(result)
                logger.info(f"{result['name']} - Success")
                products_count -= len(exception_urls) + 1
                logger.warning(f"Products exceptions: {len(exception_urls)}")
                logger.info(f"Products remaining: {products_count}")
            except Exception as exception_url:
                exception_urls.append(str(exception_url))

    with open(
        f"logs/exceptions_urls_{datetime.now()}.txt", "w", encoding="utf-8"
    ) as file:
        file.write(str(exception_urls))


if __name__ == "__main__":
    main()
