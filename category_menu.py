import requests
import csv
import os
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup

BASE_URL = 'https://www.proquinorte.com/pages/catalogo'
FILE_NAME_PREFIX = 'output'
PRODUCT_LIST_IDENTIFIER = '/collections/'
THINKING_TIME = 2
IMAGE_FOLDER = 'C:\\images\\'
categories = []
duplicated = []

def get_name(url: str):
    parts = url.split('/')
    last_part = parts[len(parts)-1]    
    return '' if last_part=='catalogo' else last_part

def get_code(url: str):
    if PRODUCT_LIST_IDENTIFIER in url:
        parts = url.split('/')
        return parts[len(parts)-1]
    else:
        return ''

def download_image(url, image_name):
    response = requests.get(url)
    #url_parts = url.split('.')
    file_extension = 'jpg'#url_parts[len(url_parts)-1]
    file_path = f'{IMAGE_FOLDER}{image_name}.{file_extension}'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully to '{file_path}'")
        return file_path
    else:
        print(f"Failed to download image from '{url}'. Status code: {response.status_code}")

def get_categories(url: str, list_to_fill):
    print(f'Scrapping page: "{url}"')
    parent = get_name(url)
    time.sleep(THINKING_TIME)
    result = []
    response = requests.get(url)    
    soup = BeautifulSoup(response.text, 'html.parser')
    grid= soup.select('.rte:not(.rte--column)')
    for g in grid:
        images = g.select('td img')
        links = g.select('td p a:not(:empty)')        
        if len(links)<1 or len(links)!= len(images):
            links = g.select('td a:has(img)')
        names = g.select('td p:not(:has(img)):not(:empty)')
        if len(names)<1:
            names = g.select('td a:not(:has(img)):not(:empty)')
        for i in range(0,len(images)):
            image = images[i].get('src','')
            link = links[i].get('href','')
            name = names[i].get_text()
            item_name = '' if PRODUCT_LIST_IDENTIFIER in link else get_name(link)
            product_list_code = get_code(link)
            item = {
                'source_url': url,
                'upper_item': parent,
                'image': image,
                'image_path': download_image(image,item_name if len(item_name)>1 else product_list_code),
                'link': link,
                'item': item_name,
                'product_list_code': product_list_code,
                'name': name
            }
            result.append(item)
            list_to_fill.append(item)
            if('/collections/' not in item['link'] and len(item['link'])>1 and get_name(item['link'])!=parent):
                # if item['link'] in duplicated:
                #     print(item)
                # else:
                duplicated.append(item['link'])
                get_categories(item['link'], list_to_fill)

get_categories(BASE_URL,categories)

current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

csv_file_path = f"{FILE_NAME_PREFIX}_{current_time}.csv"
json_file_path = f"{FILE_NAME_PREFIX}_{current_time}.json"
field_names = ['source_url', 'upper_item', 'image', 'image_path', 'link','item', 'product_list_code', 'name']

print(f'Printing the csv file: {csv_file_path}')
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    for item in categories:
        writer.writerow(item)

print(f'Printing the json file: {csv_file_path}')
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(categories, json_file, indent=4)

print(f'Process finished.')