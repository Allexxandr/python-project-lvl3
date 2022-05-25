#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from page_loader.get_request import make_parser
from page_loader.get_resources import download


def main():
    args = make_parser().parse_args()
    download(args.url,args.output)


if __name__ == '__main__':
    main()
