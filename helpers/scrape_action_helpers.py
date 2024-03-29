import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def wait_for_element_to_load(chrome_driver: webdriver.Chrome, xpath: str) -> str:
    """
    Wait for element to load searched by xpath
    :param chrome_driver: chrome web driver instance
    :param xpath: XPath
    :return: element
    """
    element = WebDriverWait(chrome_driver, 60).until(
        ec.presence_of_element_located(
            (
                By.XPATH,
                xpath,
            )
        )
    )

    return element


def scroll_down(chrome_driver: webdriver.Chrome) -> None:
    """
    Scroll down page
    :param chrome_driver: chrome web driver instance
    :return: None
    """
    y = 1000

    last_height = chrome_driver.execute_script("return document.body.scrollHeight")

    for timer in range(0, 60):
        chrome_driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 1000
        time.sleep(3)

        if y >= last_height:
            break


def hover_to_photos(chrome_driver: webdriver.Chrome, element_to_hover_over) -> None:
    """
    Hover to elements
    :param chrome_driver: chrome web driver instance
    :param element_to_hover_over: WebElement to hover
    :return: None
    """
    hover = ActionChains(chrome_driver).move_to_element(element_to_hover_over)
    hover.perform()


def find_elements_by_xpath(chrome_driver: webdriver.Chrome, xpath: str):
    """
    Retrieve web elements by xpath
    :param chrome_driver: chrome web driver instance
    :param xpath: str
    :return: web element if found
    """
    try:
        e = WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath))
        )
    except WebDriverException:
        return None

    return e


def find_element_by_xpath(chrome_driver: webdriver.Chrome, xpath: str):
    """
    Retrieve web element by xpath
    :param chrome_driver: chrome web driver instance
    :param xpath: str
    :return: web element if found
    """
    try:
        e = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
    except WebDriverException:
        return None

    return e
