import requests
import os
import re
from urllib.parse import urlparse


import argparse


def make_parser():
    
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument(
        '-o',
        '--output',
        default=os.getcwd(),
        type=str,
        help='set output directory',
    )
    
    return parser

## переименовать get_html_file_name
def get_file_name(link):
    parsed = urlparse(link)
    name = parsed._replace(scheme="").geturl()[2:]
    name = re.sub(r'[\W_]', '-', name)
    return f'{name}.html'
    
# переименовать в get_response
def get_link(link):
  response = requests.get(link);
  return response

## основной модуль. здесь должны использоваться все функции
def load(link, path):
    file_name = get_file_name(link)
    file_path = os.path.join(path, file_name)
    with open(file_path, 'a') as f:
      f.write(get_link(link).text)


def create_dir(link):
    if not os.path.exists(link):
        os.makedirs(link)







