#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from page_loader.get_request import make_parser
from page_loader.get_resources import download, configure_logger
import sys


def main():
    args = make_parser().parse_args()
    configure_logger(args.log_level)
    try:
        download(args.url, args.output)
    except Exception as e:
        if 'url' in str(e.args):
            sys.exit(1)
        elif 'Permission denied' in str(e.args):
            sys.exit(2)
    sys.exit(0)


if __name__ == '__main__':
    main()
