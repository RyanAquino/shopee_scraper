"""
Author: Ryan Aquino
Description: Scrape shopee.com products per category
"""
import os
from selenium import webdriver
from scrape_product_details_helper import get_product_details, get_product_urls


def driver():
    """
    Initialize Google Chrome driver
    :return: chrome driver instance
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximised")
    chrome_driver = (
        webdriver.Chrome("./chromedriver", options=chrome_options)
        if os.name != "nt"
        else webdriver.Chrome(options=chrome_options)
    )

    return chrome_driver


def main(chrome_driver) -> None:
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

    product_list = []

    for url in urls:
        products = get_product_urls(url, chrome_driver)
        print(f"Product Count: {len(products)}")
        product_list += products

    for product_url in product_list:
        product_details = get_product_details(product_url, chrome_driver)
        print(product_details)


if __name__ == "__main__":
    driver = driver()
    main(driver)
    driver.close()
