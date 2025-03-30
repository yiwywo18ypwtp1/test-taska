from bs4 import BeautifulSoup
import requests
import json
import re

from specs import get_specs
from export import save_to_excel, save_to_json

url = 'https://rozetka.com.ua/apple-iphone-15-128gb-black/p395460480/'

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    print(f'page loaded successful: {response.status_code}')
else:
    print(f'cant load page: {response.status_code}')



title = soup.find(class_='title__font').text

option = soup.find_all(class_='var-options')
color = option[0].find(class_='bold').text
memory = option[1].find(class_='bold').text

default_price = soup.find(class_='product-price__small').text
discount_price = soup.find(class_='product-price__big').text.strip()
item_code = ''.join(filter(str.isdigit, soup.find('div', class_='rating').find('span').text))

images = []
for img in soup.find_all('img'):
    src = img.get('src')
    if 'goods/images' in src:
        src = src.split(' ')[0]  # убираем все лишнее после нужной ссылки
        images.append(src)

item_photos = images

serial = re.search(r"\(([\w\-\/]+)\)", soup.find(class_='title__font').text).group(1)
display_res = re.search(r"\b(\d+x\d+)\b", soup.find(class_='product-about__sticky').find(class_='mt-4').text).group(1)

item_spec = get_specs()



item_details = {
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
