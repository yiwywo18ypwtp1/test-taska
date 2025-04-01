from playwright.sync_api import sync_playwright, Page
import re


def get_details(page: Page):
    page.wait_for_selector("xpath=//*[@class='desktop']//*[contains(@class, 'title__font')]")

    title_element = page.locator("xpath=//h1[contains(@class, 'title__font')]").first
    title = title_element.inner_text()

    color_element = page.locator("xpath=//div[contains(@class, 'var-options')]//span[@class='bold']").first
    color = color_element.inner_text() if color_element.count() > 0 else None

    memory_match = re.search(r'(\d+)\s*(GB|ГБ)', title, re.IGNORECASE)
    memory = f"{memory_match.group(1)} {memory_match.group(2)}" if memory_match else None

    default_price_element = page.locator("xpath=//*[contains(@class, 'product-price__small')]").first
    discount_price_element = page.locator("xpath=//*[contains(@class, 'product-price__big')]").first

    default_price = default_price_element.inner_text() if default_price_element.count() > 0 else None
    discount_price = discount_price_element.inner_text().strip() if discount_price_element.count() > 0 else None

    item_code_element = page.locator("xpath=//*[@class='desktop']//div[@class='rating text-base']//span").first
    item_code = ''.join(filter(str.isdigit, item_code_element.inner_text())) if item_code_element.count() > 0 else None

    images = []
    for img in page.locator("xpath=//img[contains(@src, 'goods/images')]").all():
        src = img.get_attribute("src")
        if src:
            images.append(src.split(' ')[0])

    serial = re.search(r"\(([\w\-\/]+)\)", title).group(1) if title else None

    display_res = None
    about_section = page.locator("xpath=//*[contains(@class, 'product-about__sticky')]").first
    if about_section.count() > 0:
        display_element = about_section.locator("xpath=.//*[contains(@class, 'mt-4')]").first
        display_text = display_element.inner_text() if display_element.count() > 0 else None
        if display_text:
            display_match = re.search(r"\b(\d+x\d+)\b", display_text)
            display_res = display_match.group(1) if display_match else None


    page.goto('https://rozetka.com.ua/ua/apple-iphone-15-128gb-black/p395460480/characteristics/')
    item_specs = get_specs(page)


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
        'item_specs': item_specs
    }


def get_specs(page: Page):
    specs = {}
    page.wait_for_selector("xpath=//main[contains(@class, 'product-tabs__content')]", timeout=30000)

    items = page.locator("xpath=//main[contains(@class, 'product-tabs__content')]//*[contains(@class, 'item')]").all()

    for item in items:
        title_element = item.locator("xpath=.//*[contains(@class, 'label')]//span").first
        value_element = item.locator("xpath=.//*[contains(@class, 'value')]").first

        if title_element.count() > 0 and value_element.count() > 0:
            title = title_element.inner_text()
            value = value_element.inner_text()
            specs[title] = value

    return specs

