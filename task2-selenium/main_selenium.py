import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

from parse_details import get_details
from parse_spec import get_specs
from export import save_to_json, save_to_excel

driver = webdriver.Chrome()

try:
    driver.get('https://rozetka.com.ua/')

    search_field = driver.find_element(By.XPATH, "//input[@name='search']")
    search_field.clear()
    search_field.send_keys("Apple iPhone 15 128GB Black", Keys.RETURN)

    # подгружаем динамические файлы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='goods-tile']"))
    )
    print("current page:", driver.title)
    driver.save_screenshot("result/images/search_results.png")

    item_tile = driver.find_element(By.XPATH, "//div[@class='goods-tile']")

    item_page = item_tile.find_element(
        By.XPATH,
        ".//*[@class='product-link']//a"
    ).get_attribute('href')
    print(item_page)

    if item_page:
        driver.get(item_page)
        print("current page:", driver.title)
    else:
        print("page unfound")

    time.sleep(3)
    print("current page:", driver.title)
    driver.save_screenshot("result/images/product_page.png")

    product_data = get_details(driver)

    # принтим детали в консоль
    for key, value in product_data.items():
        print(f'{key}: {value}')

    # експорт в xlsx
    save_to_excel(product_data)

    # експорт .json (для теста/себя)
    save_to_json(product_data)

finally:
    driver.quit()
