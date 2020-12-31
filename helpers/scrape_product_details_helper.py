import os
from bs4 import BeautifulSoup
from helpers.scrape_action_helpers import (
    hover_to_photos,
    scroll_down,
    wait_for_element_to_load,
)
from selenium import webdriver
from pathlib import Path
from datetime import datetime


def driver():
    """
    Initialize Google Chrome driver
    :return: chrome driver instance
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximised")
    chrome_options.add_argument("--incognito")
    chrome_driver = (
        webdriver.Chrome(
            Path.cwd() / "web_drivers/chromedriver.exe", options=chrome_options
        )
        if os.name == "nt"
        else webdriver.Chrome(
            Path.cwd() / "web_drivers/chromedriver", options=chrome_options
        )
    )

    return chrome_driver


def scrape_category_url_source(chrome_driver, url: str) -> str:
    """
    Returns the html source code of the category page url
    :param chrome_driver: Chrome driver instance
    :param url: source url
    :return: html page source code
    """
    chrome_driver.get(url)
    if wait_for_element_to_load(chrome_driver, "carousel-arrow"):
        scroll_down(chrome_driver)
        html_source = chrome_driver.page_source

        return html_source


def scrape_product_urls_source(chrome_driver, url: str):
    """
    Returns the html source code of the product page url

    :param chrome_driver:
    :param url:
    :return:
    """
    chrome_driver.get(url)
    if wait_for_element_to_load(chrome_driver, "qaNIZv"):
        scroll_down(chrome_driver)
        html_source = chrome_driver.page_source

        return html_source


def get_product_urls(chrome_driver, url: str) -> [str]:
    html_source = scrape_category_url_source(chrome_driver, url)
    soup = BeautifulSoup(html_source, "html.parser")
    products = soup.find_all("a", {"data-sqe": "link"})

    product_urls = []

    for product in products:
        product_urls.append(f"https://shopee.ph{product['href']}")

    return product_urls


def get_product_details(url: str) -> dict:
    """
    Get all product details
    :param url: Product URL
    :return: Product dictionary
    """
    chrome_driver = driver()
    html_source = scrape_product_urls_source(chrome_driver, url)
    soup = BeautifulSoup(html_source, "html.parser")
    product_name = _get_product_name(soup)
    product_category = _get_product_category(soup)
    product_price = _get_product_price(soup)
    product_quantity = _get_product_quantity(chrome_driver)
    product_description = _get_product_description(soup)
    product_image = _get_product_image(chrome_driver)

    chrome_driver.close()

    # With Category
    # return {
    #     product_category: {
    #         "name": product_name,
    #         "description": product_description,
    #         "price": product_price,
    #         "image": product_image,
    #         "quantity": product_quantity,
    #         "created_at": datetime.now()
    #     }
    # }

    return {
        "name": product_name,
        "description": product_description,
        "price": product_price,
        "image": product_image,
        "quantity": product_quantity,
        "created_at": datetime.now(),
    }


def _get_product_image(chrome_driver) -> str:
    """
    Retrieve product image URL
    :param chrome_driver: chrome web driver instance
    :return: product image url
    """
    product_photos = chrome_driver.find_elements_by_class_name("ZPN9uD")

    if len(product_photos) != 1:
        product_photos.pop(0)
        product_photos.reverse()

    for product_photo in product_photos:
        hover_to_photos(chrome_driver, product_photo)

    soup = BeautifulSoup(chrome_driver.page_source, "html.parser")
    item = soup.find(class_="_2JMB9h")
    item_image = item.get("style")

    if item_image:
        item_image = item_image.split(" ")[1].split('"')[1]
        return item_image
    return ""


def _get_product_price(soup) -> str:
    """
    Retrieve Product Price helper
    :param soup: product page html source
    :return: product price
    """
    item = soup.find(class_="_3n5NQx").text
    product_price = item.split("₱")[-1].replace(",", "")

    return product_price


def _get_product_name(soup) -> str:
    """
    Retrieve Product Name helper
    :param soup: product page html source
    :return: product name
    """
    item = soup.find(class_="qaNIZv")
    item_name = item.find("span").text

    return item_name


def _get_product_category(soup) -> str:
    """
    Retrieve Product Category
    :param soup: product page html source
    :return: product category
    """
    item = soup.findAll(class_="JFOy4z")
    item_category = item[1].text

    return item_category


def _get_product_description(soup) -> str:
    """
    Retrieve Product Description
    :param soup: product page html source
    :return: product description
    """
    item = soup.find(class_="_2u0jt9")
    item_description = item.find("span").text

    return item_description


def _get_product_quantity(chrome_driver) -> str:
    """
    Retrieve product quantity in string format
    :param chrome_driver: chrome web driver instance
    :return: quantity of product
    """
    quantity = chrome_driver.find_element_by_xpath(
        "//div[contains(text(),'piece available')]"
    ).text
    quantity = quantity.split()[0]

    return quantity
