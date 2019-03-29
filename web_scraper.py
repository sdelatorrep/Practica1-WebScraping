#!/usr/bin/env python3.5
# -*- coding: UTF-8 -*-


import logging
from paises_scraper import PaisesScraper


def main():
    # logging.debug("Hello!")
    scraper = PaisesScraper()
    scraper.inicio_prueba()


if __name__ == "__main__":
    log_name = "web_scraper.log"
    logging.basicConfig(filename=log_name, filemode='w', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s   %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())

    main()
