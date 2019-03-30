#!/usr/bin/env python3.5
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import logging


logging.getLogger()


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
        # self.indicadores.append("Demografia")
        self.indicadores.append("Población")
        self.indicadores.append("Tasa de natalidad")
        self.indicadores.append("Tasa de mortalidad")
        self.indicadores.append("Tasa de fecundidad")
        self.indicadores.append("Esperanza de vida al nacer")
        self.indicadores.append("Relación empleo/población")
        # self.indicadores.append("Uso Tierra")
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
        self.indicadores.append("Happiness")
        self.indicadores.append("Usuarios de internet, % de la población")
        self.indicadores.append("Accidentes con heridos")
        # logging.debug("Total indicadores: {}".format(len(self.indicadores)))

    @staticmethod
    def baja_html(url):
        pagina = requests.get(url)
        estructura = BeautifulSoup(pagina.content, "html.parser")
        return estructura

    def lista_paises_links(self):
        """
        Obtiene la URL de cada país
        :return:
        """
        estructura = self.baja_html(self.url)
        midiv = estructura.find_all("div", {"class": "container"})
        lista_paises = list()
        for link in midiv[0].find_all("a"):
            pais = list()
            pais.append(link.string)
            pais.append(self.raiz + link.get("href"))
            # logging.debug("Pais: {}".format(pais))
            lista_paises.append(pais)

        return lista_paises
    
    def buscar_links_indicadores(self, url):
        """
        Obtiene la URL de cada indicador
        :param url:
        :return:
        """
        estructura = self.baja_html(url)
        midiv = estructura.find_all("a", string=self.indicadores)
        lista_links = list()
        for link in midiv:
            lista_links.append((link.string, link.get("href")))

        indicadores_no_encontrados = self.revisar_indicadores(lista_links)
        if len(indicadores_no_encontrados) > 0:
            self.buscar_mas_indicadores(indicadores_no_encontrados, lista_links, url)
        return lista_links

    def revisar_indicadores(self, lista_links):
        """
        Revisa si están todos los indicadores en lista_links.
        :param lista_links:
        :return:
        """
        indicadores_no_encontrados = list()
        if len(lista_links) != (len(self.indicadores)):
            logging.error("Faltan indicadores! Encontrados: {}, debería haber: {}".format(len(lista_links),
                                                                                          len(self.indicadores)))
            for ind in self.indicadores:
                encontrado = False
                for links in lista_links:
                    if ind == links[0]:
                        encontrado = True
                        break
                if not encontrado:
                    indicadores_no_encontrados.append(ind)
                    logging.error("Indicador no encontrado: {}".format(ind))
        return indicadores_no_encontrados

    def buscar_mas_indicadores(self, indicadores_no_encontrados, lista_links, url):
        """
        Algunos indicadores no aparecen en la página principal y hay que ir a buscarlos a .../topics/...
        :param indicadores_no_encontrados:
        :param lista_links:
        :param url:
        :return:
        """
        estructura = self.baja_html(url)
        todos_tag_a = estructura.find_all("a")
        for tag in todos_tag_a:
            href = tag.get('href', None)
            if href is not None and "topics" in href and href.startswith('https'):
                # logging.debug("Tema: {}".format(href))
                estructura_tema = self.baja_html(href)
                mi_div = estructura_tema.find_all("a", string=self.indicadores)
                for link in mi_div:
                    encontrado = False
                    # Comprobamos que no se haya añadido ya
                    for links in lista_links:
                        if link.string == links[0]:
                            encontrado = True
                            break
                    if not encontrado:
                        # Añadir indicador
                        logging.debug("Añadir indicador: {}".format(link.string))
                        lista_links.append((link.string, link.get("href")))

        indicadores_no_encontrados = self.revisar_indicadores(lista_links)
        if len(indicadores_no_encontrados) > 0:
            logging.error("Faltan indicadores! {}".format(indicadores_no_encontrados))
            exit(1)
            
    def buscar_valores(self, url):
        """
        Recupera los datos de cada indicador
        :param buscar_valores:
        :param url:
        :return:
        """
        estructura = self.baja_html(url)
        midiv = estructura.find_all('td',{'class':None})
        # Obtenemos una lista donde el primer valor es el año
        # y el segundo el valor del indicador
        i = 0
        lista_valores= list()
        for x in midiv:
            # Inicializamos la lsita cada 2 valores
            if i % 2 == 0:
                lista_pares = list()

            lista_pares.append(x.string)

            # Añadimos a la lista de valroes cuando tenemos la dupla de datos.
            if i % 2 != 0:
                lista_valores.append(lista_pares)
            i = i + 1
        return lista_valores
    
    def lista_vacia(self):
        """
        Devuelve una lista de indicadores vacia
        :param lista_vacia:
        :return:
        """
        lista = list()
        for ind in self.indicadores:
            lista.append(0)
       
        return lista
    
    def inicio_prueba(self):
        lista_definitiva = list()
        paises = self.lista_paises_links()
        for p in paises:
            url = p[1]
            indicadores = self.buscar_links_indicadores(url)
            # Creamos lista de años y sus indicadores vacios
            def_pais = list()
            def_indicadores = list()
            for ind in indicadores:
                url = ind[1]
                valores = self.buscar_valores(url)
                #*******************************************************
                # Montamos las listas para facilitar su escritura a csv
                #*******************************************************
                pos_ind = self.indicadores.index(ind[0])
                for v in valores:
                    # Comprobamos si el año ya ha sido tratado, si no creamos la estructura
                    if v[0] in def_pais:
                        pos = def_pais.index(v[0])
                    else:
                        def_pais.append(v[0])
                        def_indicadores.append(self.lista_vacia())   
                        pos = len(def_pais)-1
                        
                        
                    # Ponemos el valor en el sitio que le pertenece.
                    def_indicadores[pos][pos_ind] = v[1] 
                    
            #*******************************************************
            # Ahora ya podemos montar una lista con pais, año, indicadores.
            #*******************************************************
            
            for i in range(len(def_pais)):
                lista = list()
                lista.append(p[0])
                lista.append(def_pais[i])
                lista.extend(def_indicadores[i]) 
                lista_definitiva.append(lista)
                
            print(lista_definitiva)
            logging.debug("URL: {}".format(url))
            logging.debug("Indicadores: {}".format(indicadores))
            break
