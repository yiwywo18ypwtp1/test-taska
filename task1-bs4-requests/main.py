from bs4 import BeautifulSoup
import requests
import json
import re

from parse_spec import get_specs
from parse_details import get_details
from export import save_to_excel, save_to_json

url = 'https://rozetka.com.ua/apple-iphone-15-128gb-black/p395460480/'

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    print(f'page loaded successful: {response.status_code}')
else:
    print(f'cant load page: {response.status_code}')


# сбор данных
item_details = get_details(soup)

# експорт в xlsx
save_to_excel(item_details)

# експорт .json (для теста/себя)
save_to_json(item_details)

# принтим в консоль
for key, value in item_details.items():
    print(f"{key}: {value}")







# DEBUG

# image_url = soup.find(class_='main-slider__wrap').find(class_='image').get('src')
# print(image_url)


# for image_url in set(images): # уникаем дубликатов
#     print(image_url)
