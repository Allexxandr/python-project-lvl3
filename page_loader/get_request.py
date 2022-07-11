import requests
import os
import re
from urllib.parse import urlparse
import logging
from functools import wraps

import argparse

log = logging.getLogger(__name__)


LEVELS = (INFO, DEBUG) = ('INFO', 'DEBUG')


def debug_logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = f'[{func.__name__:>30}]'

        log.debug(f'{func_name} :: input: {args} {kwargs}')
        res = func(*args, **kwargs)
        log.debug(f'{func_name} :: return: {str(res)}')
        return res
    return wrapper


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
    parser.add_argument(
        '-l',
        '--log-level',
        choices=LEVELS,
        default=logging.INFO,
        help='set log level',
    )
    return parser


@debug_logger
def get_file_name(link):
    parsed = urlparse(link)
    name = parsed._replace(scheme="").geturl()[2:]
    name = re.sub(r'[\W_]', '-', name)
    return f'{name}.html'


@debug_logger
def get_link(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
    except requests.HTTPError as err:
        log.exception(
          str(err.args),
          exc_info=log.getEffectiveLevel() == logging.DEBUG,
        )
        raise
    return response


def load(link, path):

    file_name = get_file_name(link)
    file_path = os.path.join(path, file_name)
    try:
        with open(file_path, 'a') as f:
            f.write(get_link(link).text)
    except PermissionError:
        log.exception(
            'Permission denied',
            exc_info=log.getEffectiveLevel() == logging.DEBUG,
          )
        raise


@debug_logger
def create_dir(link):
    if not os.path.exists(link):
        os.makedirs(link)
