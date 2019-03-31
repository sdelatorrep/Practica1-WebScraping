#!/usr/bin/env python3.5
# -*- coding: UTF-8 -*-


import logging
from paises_scraper import PaisesScraper


def main():
    logging.debug("Inicio web scraping")

    scraper = PaisesScraper()
    scraper.obtener_datos("indicadores.csv")
    # scraper.obtener_datos_con_diccionarios("indicadores_v2.csv")

    logging.debug("Fin web scraping")


if __name__ == "__main__":
    log_name = "web_scraper.log"
    logging.basicConfig(filename=log_name, filemode='w', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s   %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())

    main()
