import requests
import os
import os.path
import re
from urllib.parse import urlparse
from page_loader.get_request import get_file_name, get_link, load
from bs4 import BeautifulSoup

def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_local_url(url, site_url):
    if not is_url(url):
        return True
    else:
        return urlparse(url).netloc == site_url


LIST_RESOURCES = {  # noqa: 407
    'link': 'href',
    'script': 'src',
    'img': 'src',
}


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_resources_dir_name(path):
    return path.replace('.html', '_files')
	
	
def create_resource_name(original_name, site_url):
    base, ext = os.path.splitext(original_name)
    base = re.sub(r'[\W_]', '-', base)
    site_url = re.sub(r'[\W_]', '-', site_url)
    return f'{site_url}-{base}{ext}'

def find_resources(soup, path, site_url): 
    
    resources = []
    for tag, attr in LIST_RESOURCES.items():
        for node in soup.find_all(tag):
            
            attr_val = node.get(attr)
            if attr_val is not None and is_local_url(attr_val, site_url):
                base, ext = os.path.splitext(attr_val)
                if ext:
                    new_attr_val = create_resource_name(attr_val, site_url)
                    resources.append(
                        {'old_value': attr_val, 'new_value': new_attr_val},
                    )
                    node[attr] = os.path.join(path, new_attr_val)
    
    return resources

def download_resources(resources, base_url, resources_dir_name):
    create_dir(resources_dir_name)
    for r in resources:
        url = f'{base_url}{r["old_value"]}'
        print(url)
        file_path = os.path.join(resources_dir_name, r['new_value'])
        # print(get_link(url).content)
        with open(file_path, 'wb') as f:
            f.write(requests.get(url, stream=True).content)

## поменять местами аргументы
def download(url, output):
    url = url.rstrip('/')
    html_file_path = os.path.join(output, get_file_name(url))
    # использовать os.path.join
    resources_dir_name = get_resources_dir_name(html_file_path)
    parsed_url = urlparse(url)
    site_url = parsed_url.netloc
    resources = find_resources(
        # вынести в переменную soup
        BeautifulSoup(get_link(url).content, 'html.parser'), 
        resources_dir_name, site_url
    )
    

    load(url, output)
    if resources:
        download_resources(
            resources,
            url,
            resources_dir_name,
        )

    


