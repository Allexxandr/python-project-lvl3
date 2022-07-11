import re


def file_name(link):
    name = re.sub(r'[\W_]', '-', link)
    return f'{name}.html'
