from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

from selenium.webdriver.support.wait import WebDriverWait

from parse_spec import get_specs


def get_details(driver):
    # Ожидание загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'title__font')]"))
    )

    title = driver.find_element(By.XPATH, "//h1[contains(@class, 'title__font')]").text

    # цвет
    try:
        color = driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'var-options')]//span[@class='bold']"
        ).text
    except NoSuchElementException:
        color = None

    # память
    memory = None
    title = driver.find_element(By.XPATH, "//h1[contains(@class, 'title__font')]").text
    memory_match = re.search(r'(\d+)\s*(GB|ГБ)', title, re.IGNORECASE)
    if memory_match:
        memory = f"{memory_match.group(1)} {memory_match.group(2)}"

    # цена
    try:
        default_price = driver.find_element(By.XPATH, "//*[contains(@class, 'product-price__small')]").text
        discount_price = driver.find_element(By.XPATH, "//*[contains(@class, 'product-price__big')]").text.strip()
    except NoSuchElementException:
        default_price, discount_price = None, None

    # код
    try:
        # тут у меня была проблема в том, что
        # <span _ngcontent-rz-client-c3166959541 class="ms-auto color-black-60"> Код: &nbsp;395460480 </span>
        # в верстке розетки 2: для десктопа и для телефона
        # и из за этого я не мог вытянуть код =)
        item_code = driver.find_element(By.XPATH, "//*[@class='desktop']//div[@class='rating text-base']//span").text
        item_code = ''.join(filter(str.isdigit, item_code))
    except NoSuchElementException as e:
        item_code = None

    # картинки
    images = []
    for img in driver.find_elements(By.XPATH, "//img[contains(@src, 'goods/images')]"):
        src = img.get_attribute('src')
        if src:
            images.append(src.split(' ')[0])

    # серийный номер
    serial = re.search(r"\(([\w\-\/]+)\)", title).group(1) if title else None

    # дисплей
    try:
        about_section = driver.find_element(By.XPATH, "//*[contains(@class, 'product-about__sticky')]")
        display_text = about_section.find_element(By.XPATH, ".//*[contains(@class, 'mt-4')]").text
        display_res = re.search(r"\b(\d+x\d+)\b", display_text).group(1) if display_text else None
    except NoSuchElementException:
        display_res = None

    # характеристики
    # _driver = driver.get(driver)
    # item_specs = get_specs(_driver)

    return {
        'title': title,
        'color': color,
        'memory': memory,
        'default_price': default_price,
        'discount_price': discount_price,
        'item_code': item_code,
        'images': images,
        'serial': serial,
        'display_resolution': display_res,
        # 'item_specs': item_specs
    }