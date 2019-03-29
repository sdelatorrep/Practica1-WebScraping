#!/usr/bin/env python3.5
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests


class PaisesScraper:

    def __init__(self):
        self.url = "https://knoema.es/atlas"
        self.raiz = "https://knoema.es"
        self.indicadores = list()
        self.lista_indicadores()

    def lista_indicadores(self):
        self.indicadores.append("PIB")
        self.indicadores.append("Inflación del IPC")
        self.indicadores.append("Tasa de desempleo")
        self.indicadores.append("Importaciones de bienes y servicios")
        self.indicadores.append("Exportaciones de bienes y servicios")
        self.indicadores.append("Demografia")
        self.indicadores.append("Población")
        self.indicadores.append("Tasa de natalidad")
        self.indicadores.append("Tasa de mortalidad")
        self.indicadores.append("Tasa de fecundidad")
        self.indicadores.append("Esperanza de vida al nacer")
        self.indicadores.append("Relación empleo/población")
        self.indicadores.append("Uso Tierra")
        self.indicadores.append("Terrenos agrícolas (km2)")
        self.indicadores.append("Zona forestal")
        self.indicadores.append("Mortalidad infantil")
        self.indicadores.append("Gasto en salud, % del PIB")
        self.indicadores.append("Gasto en salud per cápita")
        self.indicadores.append("Gasto militar, US$ actual")
        self.indicadores.append("Gasto militar, % del PIB")
        self.indicadores.append("Gasto público en eduación")
        self.indicadores.append("Tasa de Homicidios")
        self.indicadores.append("Ingresos por turismo")
        self.indicadores.append("Gasto en investigación y desarrollo, % del PIB")
        self.indicadores.append("Índice de Desarrollo Humano")
        self.indicadores.append("Felicidad")
        self.indicadores.append("Usuarios de internet, % de la población")
        self.indicadores.append("Accidentes con heridos (tráfico)")

    @staticmethod
    def baja_html(url):
        pagina = requests.get(url)
        estructura = BeautifulSoup(pagina.content, "html.parser")
        return estructura

    def lista_paises_links(self):
        estructura = self.baja_html(self.url)
        midiv = estructura.find_all("div", {"class": "container"})
        lista_paises = list()
        for link in midiv[0].find_all("a"):
            pais = list()
            pais.append(link.string)
            pais.append(self.raiz+link.get("href"))
            lista_paises.append(pais)
        return lista_paises
    
    def lista_indicadores_links(self, url):
        estructura = self.baja_html(url)
        midiv = estructura.find_all("a", string=self.indicadores)
        lista_links = list()
        for link in midiv:
            indicador = list()
            indicador.append(link.string)
            indicador.append(link.get("href"))
            lista_links.append(indicador)
        return lista_links

    def inicio_prueba(self):
        paises = self.lista_paises_links()
        for p in paises:
            url = p[1]
            indicadores = self.lista_indicadores_links(url)
            print(url)
            print(indicadores)
            break
