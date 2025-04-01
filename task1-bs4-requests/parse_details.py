from bs4 import BeautifulSoup
import requests
import json
import re

from parse_spec import get_specs


def get_details(soup):
    try:
        title = soup.find(class_='title__font').text
    except (AttributeError, AssertionError):
        title = None

    try:
        option = soup.find_all(class_='var-options')
        color = option[0].find(class_='bold').text
        memory = option[1].find(class_='bold').text
    except (AttributeError, AssertionError, IndexError):
        color = None
        memory = None

    try:
        default_price = soup.find(class_='product-price__small').text
        discount_price = soup.find(class_='product-price__big').text.strip()
    except (AttributeError, AssertionError):
        default_price = None
        discount_price = None

    try:
        item_code = ''.join(filter(str.isdigit, soup.find('div', class_='rating').find('span').text))
    except (AttributeError, AssertionError):
        item_code = None

    try:
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if 'goods/images' in src:
                src = src.split(' ')[0]  # убираем все лишнее после нужной ссылки
                images.append(src)

        item_photos = images
    except (AttributeError, AssertionError):
        item_photos = []

    try:
        serial = re.search(r"\(([\w\-\/]+)\)", soup.find(class_='title__font').text).group(1)
    except (AttributeError, AssertionError):
        serial = None

    try:
        display_res = re.search(r"\b(\d+x\d+)\b",
                                soup.find(class_='product-about__sticky').find(class_='mt-4').text).group(1)
    except (AttributeError, AssertionError):
        display_res = None

    try:
        item_spec = get_specs()
    except Exception as e:
        item_spec = None
        print(f"cant get specs - {e}")

    return {
        'title': title,
        'color': color,
        'memory_volume': memory,
        'default_price': default_price,
        'discount_price': discount_price,
        'item_code': item_code,
        'item_photos': item_photos,
        'serial': serial,
        'display_res': display_res,
        'item_specs': item_spec,
    }
