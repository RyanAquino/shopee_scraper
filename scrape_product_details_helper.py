from bs4 import BeautifulSoup
from scrape_action_helpers import hover_to_photos, scroll_down, wait_for_products_load
import time


def scrape_category_url_source(chrome_driver, url) -> str:
    """
    Returns the html source code of the category page url

    :param chrome_driver: Chrome driver instance
    :param url: source url
    :return: html page source code
    """
    chrome_driver.get(url)
    if wait_for_products_load(chrome_driver):
        scroll_down(chrome_driver)
        html_source = chrome_driver.page_source

        return html_source


def scrape_product_urls_source(chrome_driver, url):
    """
    Returns the html source code of the product page url

    :param chrome_driver:
    :param url:
    :return:
    """
    chrome_driver.get(url)
    scroll_down(chrome_driver)
    html_source = chrome_driver.page_source

    return html_source


def get_product_urls(url, chrome_driver) -> [str]:
    html_source = scrape_category_url_source(chrome_driver, url)
    soup = BeautifulSoup(html_source, "html.parser")
    products = soup.find_all("a", {"data-sqe": "link"})

    product_urls = []

    for product in products:
        product_urls.append(f"https://shopee.ph{product['href']}")

    return product_urls


def get_product_details(url, chrome_driver) -> dict:
    html_source = scrape_product_urls_source(chrome_driver, url)
    soup = BeautifulSoup(html_source, "html.parser")
    product_name = _get_product_name(soup)
    product_category = _get_product_category(soup)
    product_price = soup.find(class_="_3n5NQx").text
    product_quantity = _get_product_quantity(chrome_driver)
    product_description = _get_product_description(soup)
    product_image = _get_product_image(chrome_driver)

    return {
        product_category: {
            "name": product_name,
            "description": product_description,
            "price": product_price,
            "created_at": time.localtime(),
            "quantity": product_quantity,
            "image": product_image,
        }
    }


def _get_product_image(chrome_driver):
    product_photos = chrome_driver.find_elements_by_class_name("ZPN9uD")

    for product_photo in product_photos:
        hover_to_photos(chrome_driver, product_photo)

    soup = BeautifulSoup(chrome_driver.page_source, "html.parser")
    item = soup.find(class_="_2JMB9h")
    item_image = item.get("style").split(" ")[1].split('"')[1]

    return item_image


def _get_product_name(soup):
    item = soup.find(class_="qaNIZv")
    item_name = item.find("span").text

    return item_name


def _get_product_category(soup):
    item = soup.findAll(class_="JFOy4z")
    item_category = item[1].text

    return item_category


def _get_product_description(soup):
    item = soup.find(class_="_2u0jt9")
    item_description = item.find("span").text

    return item_description


def _get_product_quantity(chrome_driver):
    quantity = chrome_driver.find_element_by_xpath(
        "//div[contains(text(),'piece available')]"
    ).text
    quantity = quantity.split()[0]

    return quantity
