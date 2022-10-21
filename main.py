#from EstadaoCrawler import EstadaoCrawler

import os
from abcDoAbcCrawler import abcDoAbcCrawler

"""    'Pos+Balsa',
    'Riacho+Grande',
    'Tatetos',
    'Taquacetuba',
    'Santa+Cruz',
    'Capivari',
    'Capivari+Pos+Balsa',
    'Capivari+Riacho+Grande',
    'Capivari+Tatetos',
    'Capivari+Taquacetuba',
    'Capivari+Santa+Cruz',
    'Curucutu',
    'Curucutu+Pos+Balsa',
    'Curucutu+Riacho+Grande',
    'Curucutu+Tatetos',
    'Curucutu+Taquacetuba',
    'Curucutu+Santa+Cruz'"""

termos_de_pesquisa = [
    'Pos+Balsa',
    'Riacho+Grande',
    'Tatetos',
    'Taquacetuba',
    'Santa+Cruz',
    'Capivari',
    'Capivari+Pos+Balsa',
    'Capivari+Riacho+Grande',
    'Capivari+Tatetos',
    'Capivari+Taquacetuba',
    'Capivari+Santa+Cruz',
    'Curucutu',
    'Curucutu+Pos+Balsa',
    'Curucutu+Riacho+Grande',
    'Curucutu+Tatetos',
    'Curucutu+Taquacetuba',
    'Curucutu+Santa+Cruz'
    ]
periodo = {
    'inicio': '01.06.2021',
    'fim': '01.02.2022'
}
periodo = '{}%2F{}%2F{}-{}%2F{}%2F{}'.format(periodo['inicio'][0:2], periodo['inicio'][3:5], periodo['inicio'][6:],
                                             periodo['fim'][0:2], periodo['fim'][3:5], periodo['fim'][6:])

for termo in termos_de_pesquisa:
    
    crawler = abcDoAbcCrawler(termo, periodo)

    os.makedirs("D:\crawler_abcdoabc\{}".format(termo))
    
    try:
        crawler.iniciar_pesquisa()
        crawler.capturar_links()
        crawler.raspar_noticia()
    except:
        print("nenhum resultado")
        crawler.driver.close()

    
    
