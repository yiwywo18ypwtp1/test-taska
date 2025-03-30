from bs4 import BeautifulSoup
import requests
import json
import re

url = 'https://rozetka.com.ua/ua/apple-iphone-15-128gb-black/p395460480/characteristics/'

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    print(f'page loaded successful: {response.status_code}')
else:
    print(f'cant load page: {response.status_code}')

characteristics = soup.find(class_='product-tabs__content').find_all(class_='item')


def get_specs():
    item_characteristics = {}

    for item in characteristics:
        title = item.find(class_='label').find('span').text
        value = item.find(class_='value').text
        # print(f"{title}: {value}")

        item_characteristics[title] = value

    return item_characteristics
