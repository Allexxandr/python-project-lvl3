import requests
import os
import os.path
import re
from urllib.parse import urlparse
from page_loader.get_request import get_file_name, get_link, load
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
import logging
import sys
# from tests.test_loader import HTTPResponseException

log = logging.getLogger(__name__)


def configure_logger(log_level):

    log_format = '[ %(levelname)-5.5s ] :: %(message)s'
    logging.basicConfig(
        handlers=[logging.StreamHandler(sys.stdout)],
        format=log_format,
        level=logging.getLevelName(log_level),
    )


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


def strip_scheme(url):
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)


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
    # print('>>>', site_url, base, ext, f'{site_url}{base}{ext}')
    return f'{site_url}{base}{ext}'


def find_resources(soup, path, site_url):
    resources = []
    for tag, attr in LIST_RESOURCES.items():
        for node in soup.find_all(tag):
            attr_val = node.get(attr)
            if attr_val is not None and attr_val.startswith('/'):
                base, ext = os.path.splitext(attr_val)
                if attr_val.__contains__('http'):
                    base, ext = os.path.splitext(strip_scheme(attr_val))

                if ext:
                    new_attr_val = create_resource_name(attr_val, site_url)
                    resources.append(
                        {'old_value': attr_val, 'new_value': new_attr_val},
                    )
                    node[attr] = os.path.join(path, new_attr_val)

    return resources


def download_resources(resources, base_url, resources_dir_name):
    create_dir(resources_dir_name)
    total_items = len(resources)

    with IncrementalBar('Downloading:', max=total_items) as progbar:
        progbar.suffix = '%(percent).1f%% (eta: %(eta)s)'

        for r in resources:
            url = f'{base_url}{r["old_value"]}'
            file_path = os.path.join(resources_dir_name, r['new_value'])

            with open(file_path, 'wb') as f:
                f.write(requests.get(url, stream=True).content)
                progbar.next()


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
    log.info(f'Done. You can open saved page from: {html_file_path}')
    logger = configure_logger

    load(url, output)
    try:

        if resources:
            download_resources(
                resources,
                url,
                resources_dir_name,
            )

        return html_file_path

    except requests.ConnectionError as e:
        message = f'Reponse error. {e.message}'
        print(message)
    except FileNotFoundError as e:
        message = f'File or directory {e.filename} not found on the disk'
        logger.error(message)
    except FileExistsError as e:
        message = f'File or directory {e.filename} already exists'
        logger.error(message)
    except PermissionError as e:
        message = f'Can\'t access {e.filename}'
        logger.error(message)

        sys.exit(20)


LEVELS = (INFO, DEBUG) = ('INFO', 'DEBUG')
