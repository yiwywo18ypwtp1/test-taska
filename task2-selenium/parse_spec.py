from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def get_specs(driver):
    item_characteristics = {}

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//main[contains(@class, 'product-tabs__content')]"))
        )

        items = driver.find_elements(By.XPATH,
                                     "//main[contains(@class, 'product-tabs__content')]//*[contains(@class, 'item')]")

        for item in items:
            try:
                title = item.find_element(By.XPATH, ".//*[contains(@class, 'label')]//span").text

                value = item.find_element(By.XPATH, ".//*[contains(@class, 'value')]").text

                item_characteristics[title] = value

            except NoSuchElementException:
                continue

    except TimeoutException:
        print("timeout except")
    except Exception as e:
        print(f"parse error: {str(e)}")

    return item_characteristics
