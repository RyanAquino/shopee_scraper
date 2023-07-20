import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

config = {
    "PRODUCT_CONTAINER": "//div[contains(@id, 'main')]/div/div[2]/div/div/div[4]",
    "PRODUCT_DETAILS": "//div[contains(@class, 'product-briefing')]",
    "PRODUCT_CATEGORY": "//div[contains(@class, 'page-product')]/div/div[1]/a[2]",
    "PRODUCT_PRICE": "//div[contains(@class, 'product-briefing')]/div[3]/div/div[3]/div/div/div[1]/div/div",
    "PRODUCT_DESCRIPTION": "//div[contains(@class, 'product-detail')]/div[last()]/div[last()]/div",
    "PRODUCT_PHOTOS": "//div[contains(@class, 'product-briefing')]/div[2]/div[1]/div[2]/div",
    "PRODUCT_DETAIL_PHOTO": "//div[contains(@class, 'product-briefing')]/div[2]/div[1]/div[1]/div/div[last()]/div",
    "PRODUCT_NAME": "//div[contains(@class, 'product-briefing')]/div[3]/div/div[1]",
    **os.environ,
}
