from datetime import datetime

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver

from elements_config import config
from helpers.scrape_action_helpers import (
    find_element_by_xpath,
    find_elements_by_xpath,
    hover_to_photos,
    scroll_down,
    wait_for_element_to_load,
)


def driver() -> webdriver.Chrome:
    """
    Initialize Google Chrome browser options
    :return: Google Chrome instance
    """
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--incognito")

    return uc.Chrome(
        use_subprocess=False,
        options=chrome_options,
        user_multi_procs=True,
        browser_executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    )


def scrape_category_url_source(chrome_driver: webdriver.Chrome, url: str) -> str:
    """
    Returns the html source code of the category page url
    :param chrome_driver: Chrome driver instance
    :param url: source url
    :return: html page source code
    """
    chrome_driver.get(url)

    if wait_for_element_to_load(chrome_driver, config["PRODUCT_CONTAINER"]):
        scroll_down(chrome_driver)
        html_source = chrome_driver.page_source

        return html_source


def scrape_product_urls_source(chrome_driver: webdriver.Chrome, url: str):
    """
    Returns the html source code of the product page url

    :param chrome_driver: Chrome driver instance
    :param url: URL string
    :return: HTML source
    """
    chrome_driver.get(url)
    if wait_for_element_to_load(chrome_driver, config["PRODUCT_DETAILS"]):
        scroll_down(chrome_driver)
        if wait_products_elements(chrome_driver):
            html_source = chrome_driver.page_source

            return html_source


def get_product_urls(chrome_driver: webdriver.Chrome, url: str) -> [str]:
    """
    Get product URLs
    :param chrome_driver: Chrome driver instance
    :param url: product category URL
    :return: list of product URLs
    """
    html_source = scrape_category_url_source(chrome_driver, url)
    soup = BeautifulSoup(html_source, "html.parser")
    products = soup.find_all("a", {"data-sqe": "link"})

    product_urls = []

    for product in products:
        product_urls.append(f"https://shopee.ph{product['href']}")

    return product_urls


def wait_products_elements(chrome_driver: webdriver.Chrome) -> bool:
    """
    Wait for product elements to be loaded.
    :param chrome_driver: Chrome driver instance
    :return: True if all elements are loaded else False
    """
    product_category = wait_for_element_to_load(
        chrome_driver, config["PRODUCT_CATEGORY"]
    )
    product_price = wait_for_element_to_load(chrome_driver, config["PRODUCT_PRICE"])
    product_description = wait_for_element_to_load(
        chrome_driver, config["PRODUCT_DESCRIPTION"]
    )

    return all([product_category, product_price, product_description])


def get_product_details(url: str) -> dict:
    """
    Get all product details
    :param url: Product URL
    :return: Product dictionary
    """
    chrome_driver = driver()
    try:
        if not scrape_product_urls_source(chrome_driver, url):
            return {}
        product_name = _get_product_name(chrome_driver)
        product_category = _get_product_category(chrome_driver)  # noqa: F841
        product_price = _get_product_price(chrome_driver)
        product_quantity = _get_product_quantity(chrome_driver)
        product_description = _get_product_description(chrome_driver)
        product_image = _get_product_image(chrome_driver)
    except Exception as e:
        print(str(e))
        raise Exception(url)
    finally:
        chrome_driver.quit()

    # With Category
    # return {
    #     product_category: {
    #         "name": product_name,
    #         "description": product_description,
    #         "price": product_price,
    #         "image_url": product_image,
    #         "quantity": product_quantity,
    #         "created_at": datetime.now()
    #     }
    # }

    return {
        "name": product_name,
        "description": product_description,
        "price": product_price,
        "image_url": product_image,
        "quantity": product_quantity,
        "created_at": datetime.now(),
    }


def _get_product_image(chrome_driver: webdriver.Chrome) -> str:
    """
    Retrieve product image URL
    :param chrome_driver: chrome web driver instance
    :return: product image url
    """

    product_photos = find_elements_by_xpath(chrome_driver, config["PRODUCT_PHOTOS"])
    item = None
    item_image = None

    if len(product_photos) != 1:
        product_photos.reverse()

    while product_photos and not item_image:
        for product_photo in product_photos:
            hover_to_photos(chrome_driver, product_photo)

        item = find_element_by_xpath(chrome_driver, config["PRODUCT_DETAIL_PHOTO"])

        if item:
            break
        else:
            product_photos.pop()

    if not item:
        return item

    item_image = item.get_attribute("style")

    if item_image:
        item_image = item_image.split(" ")[1].split('"')[1]

    return item_image


def _get_product_price(chrome_driver: webdriver.Chrome) -> str:
    """
    Retrieve Product Price helper
    :param chrome_driver: chrome web driver instance
    :return: product price
    """
    product_price_xpath = config["PRODUCT_PRICE"]
    item = find_element_by_xpath(chrome_driver, product_price_xpath).text

    product_price = item.split("₱")[-1].replace(",", "")

    return product_price or 0


def _get_product_name(chrome_driver: webdriver.Chrome) -> str:
    """
    Retrieve Product Name helper
    :param chrome_driver: chrome web driver instance
    :return: product name
    """
    product_name_xpath = config["PRODUCT_NAME"]
    item = find_element_by_xpath(chrome_driver, product_name_xpath)

    return item.text


def _get_product_category(chrome_driver: webdriver.Chrome) -> str:
    """
    Retrieve Product Category
    :param chrome_driver: chrome web driver instance
    :return: product category
    """
    product_category_xpath = config["PRODUCT_CATEGORY"]
    item_category = find_element_by_xpath(chrome_driver, product_category_xpath)

    return item_category.text


def _get_product_description(chrome_driver: webdriver.Chrome) -> str:
    """
    Retrieve Product Description
    :param chrome_driver: Chrome web driver instance
    :return: product description
    """
    item = find_element_by_xpath(chrome_driver, config["PRODUCT_DESCRIPTION"])

    if not item:
        return ""

    return item.text


def _get_product_quantity(chrome_driver: webdriver.Chrome) -> str:
    """
    Retrieve product quantity in string format
    :param chrome_driver: Chrome web driver instance
    :return: quantity of product
    """
    quantity = find_element_by_xpath(
        chrome_driver, "//div[contains(text(),'pieces available')]"
    ).text
    quantity = quantity.split()[0]

    return quantity
