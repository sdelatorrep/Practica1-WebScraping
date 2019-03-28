from bs4 import BeautifulSoup
import requests

class PaisesScrapper():

    def __init__(self):
        self.url = "https://knoema.es/atlas"

    def __Baja_HTML(self, url):
        pagina = requests.get(url)
        estructura = BeautifulSoup(pagina.content, "html.parser")
        return estructura

    def __lista_paises_links(self):
        esructura = self.__Baja_HTML(self.url)
        estructura.findAll('div')
        midiv = estructura.find_all('div',{'class':'container'})
        m = midiv[0]
        lista_paises=[]
        for link in m.find_all('a'):
            pais = []
            pais.append(link.string)
            pais.append(url+link.get('href'))
            lista_paises.append(pais)
        return lista_paises
