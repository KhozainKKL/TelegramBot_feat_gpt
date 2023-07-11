import csv
import json
import os
import random
import requests
from time import sleep
import time
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import re
from urllib.parse import quote

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.58',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.7'
}


### Асинхронное выполнение кода ###


# async def get_soup(session, url):
#     async with session.get(url, headers=HEADERS, timeout=1000) as response:
#         if response.status != 200:
#             return None
#         html = await response.text()
#         soup = BeautifulSoup(html, 'lxml')
#         return soup
#
#
# async def get_products(session, category_url):
#     tasks = []
#     products = {}
#     for i in range(1, 1000):
#         task = asyncio.create_task(get_soup(session, f"{category_url}?PAGEN_1={i}"))
#         tasks.append(task)
#     soup_list = await asyncio.gather(*tasks)
#     for soup in soup_list:
#         if not soup:
#             continue
#         count_all_product_in_list = soup.find_all(class_='item_info TYPE_1')
#         for item in count_all_product_in_list:
#             print(count_all_product_in_list)
#             """собираем все товары в данном каталоге на странице"""
#             product_name = item.find(class_='item-title').find('a').text
#             product_href = 'https://vdd36.ru' + item.find('a').get('href')
#             product_article = item.find(class_='article_block').get('data-value')
#             product_price = item.find(class_='price_value').text + item.find(
#                 class_='price_currency').text + item.find(
#                 class_='price_measure').text
#             products = {
#                 'Название продукта': product_name,
#                 'Артикул': product_article,
#                 'Цена товара': product_price,
#                 'Адрес товара': product_href
#             }
#             await asyncio.sleep(random.uniform(10, 20))
#     return products
#
#
# async def main():
#     all_categories_dict = {}
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://vdd36.ru/', headers=HEADERS, timeout=1000) as response:
#             html = await response.text()
#             soup = BeautifulSoup(html, 'lxml')
#             all_categories = soup.find_all(class_='icons_fa')
#             for item in all_categories:
#                 item_text = item.text.strip()
#                 item_href = 'https://vdd36.ru' + item.get('href')
#                 all_categories_dict[item_text] = item_href
#                 with open('templates/tovari_dlya_doma/all_categories.json', 'w', encoding='utf-8') as file:
#                     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)
#             with open('templates/tovari_dlya_doma/all_categories.json', encoding='utf-8') as file:
#                 all_categories = json.load(file)
#             iteration_count = len(all_categories)
#             print(f'Всего итераций: {iteration_count}')
#             count = 0
#             for category_name, category_href in all_categories.items():
#                 """Переименовываем все названия катал"""
#                 category_name_en = category_name.replace(' ', '_')
#                 print(f'Обработка каталога: {category_name_en}')
#                 products = await get_products(session, category_href)
#                 count += 1
#                 with open(f'templates/tovari_dlya_doma/{category_name_en}.csv', 'w', newline='',
#                           encoding='utf-8') as file:
#                     writer = csv.DictWriter(file, fieldnames=products.keys())
#                 writer.writeheader()
#                 writer.writerows(products)
#                 print(f'Каталог {category_name_en} обработан ({count}/{iteration_count})')
#                 await asyncio.sleep(random.uniform(10, 20))
#
#
# if __name__ == '__main__':
#     start_time = time.time()
#     asyncio.run(main())
#     print(f'Время выполнения: {time.time() - start_time} секунд')

### ОСНОВНОЕ ВЫПОЛНЕНИЕ КОДА ###


# def get_data(url):
#     headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
#                              '(KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.58',
#                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
#                          'q=0.8,application/signed-exchange;v=b3;q=0.7'}
#
#     req = requests.get(url=url, headers=headers)
#     src = req.text
#
#     soup = BeautifulSoup(src, 'lxml')
#     all_categories = soup.find_all(class_='icons_fa')
#
#     """Ищем все каталоги продуктов сайта"""
#     all_categories_dict = {}
#     for item in all_categories:
#         item_text = item.text.strip()
#         item_href = 'https://vdd36.ru' + item.get('href')
#
#         all_categories_dict[item_text] = item_href
#
#         """Записываем все найденные каталоги продуктов"""
#         with open('templates/tovari_dlya_doma/all_categories.json', 'w', encoding='utf-8') as file:
#             json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)
#
#     """Обращаемся к загруженным каталогам чтобы не нагружать сайт"""
#     with open('templates/tovari_dlya_doma/all_categories.json', encoding='utf-8') as file:
#         all_categories = json.load(file)
#
#     iteration_count = int(len(all_categories)) - 1
#     count = 0
#     print(f'Всего итераций: {iteration_count}')  # <-------------
#
#     for category_name, category_href in all_categories.items():
#         """Переименовываем все названия каталогов в файле json"""
#         rep = [',', ' ', '-']
#         for item in rep:
#             if item in category_name:
#                 category_name = category_name.replace(item, '_')
#
#         for i in range(1, 1000):
#             req = requests.get(url=category_href + f'?PAGEN_1={i}', headers=headers, timeout=100)
#             src = req.text
#
#             """ Проверка страницы на наличие таблицы с продуктами """
#             if req.status_code != 200:
#                 continue
#
#             soup = BeautifulSoup(src, 'lxml')
#
#             count_all_product_in_list = soup.find_all(class_='item_info TYPE_1')
#             for item in count_all_product_in_list:
#                 """собираем все товары в данном каталоге на странице"""
#                 product_name = item.find(class_='item-title').find('a').text
#                 product_href = 'https://vdd36.ru' + item.find('a').get('href')
#                 product_article = item.find(class_='article_block').get('data-value')
#                 product_price = item.find(class_='price_value').text + item.find(
#                     class_='price_currency').text + item.find(
#                     class_='price_measure').text
#
#                 all_categories_dict = {
#                     'Название продукта': product_name,
#                     'Артикул': product_article,
#                     'Цена товара': product_price,
#                     'Адрес товара': product_href
#                 },
#                 with open(f'templates/tovari_dlya_doma/catalogi_tovarov/{count}_{category_name}.json', 'a',
#                           encoding='utf-8') as file:
#                     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)
#
#                 sleep(random.randrange(5, 10))
#             print(f'Страница: {i}; Товара: {category_name} записан...')
#         count += 1
#
#         print(f'Итерация {count}. {category_name} записан...')
#         iteration_count -= 1
#
#         if iteration_count == 0:
#             print('Работа завершена.')
#             break
#
#         print(f'Оастлось итераций: {iteration_count}')
#         sleep(random.randrange(2, 4))

#
def get_data(what_search: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.58',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                         'q=0.8,application/signed-exchange;v=b3;q=0.7'}

    url = f'https://vdd36.ru/catalog/?q={quote(what_search, encoding="windows-1251")}&s=%CD%E0%E9%F2%E8'

    if not os.path.exists(f"parsing/templates/tovari_dlya_doma/catalogi_tovarov/{what_search}.csv"):
        with open(f'parsing/templates/tovari_dlya_doma/catalogi_tovarov/{what_search}.csv', 'w',
                  encoding='cp1251') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    'Название продукта',
                    'Артикул',
                    'Цена товара',
                    'Адрес товара'
                )
            )

    for i in range(1, 2):
        req = requests.get(url=url + f'&&PAGEN_2={i}', headers=headers, timeout=100)
        src = req.text

        """ Проверка страницы на наличие таблицы с продуктами """
        if req.status_code != 200:
            continue

        soup = BeautifulSoup(src, 'lxml')

        count_all_product_in_list = soup.find_all(class_='item_info TYPE_1')
        for item in count_all_product_in_list:
            """собираем все товары в данном каталоге на странице"""
            product_name = item.find(class_='item-title').find('a').text
            product_href = 'https://vdd36.ru' + item.find('a').get('href')
            product_article = item.find(class_='article_block').get('data-value')
            product_price = item.find(class_='price_value').text + item.find(
                class_='price_currency').text + item.find(
                class_='price_measure').text

            all_categories_dict = {
                'Название продукта': product_name,
                'Артикул': product_article,
                'Цена товара': product_price,
                'Адрес товара': product_href
            }
            with open(f'parsing/templates/tovari_dlya_doma/catalogi_tovarov/{what_search}.csv', 'a',
                      encoding='cp1251') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product_name,
                        product_article,
                        product_price,
                        product_href
                    )
                )
            sleep(random.randrange(2, 4))
        print(f'Страница {i}, Товара: {what_search} записано...')

    with open(f'parsing/templates/tovari_dlya_doma/catalogi_tovarov/{what_search}.csv', 'rb') as file:
        src = file.read()
    return src
