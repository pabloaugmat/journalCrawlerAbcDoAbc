from importlib.resources import path
from logging import exception
import shutil
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class abcDoAbcCrawler:

    def __init__(self, termo, periodo) -> None:

        self.termos_da_pesquisa = termo
        self.periodo = periodo
        self.driver = None
        self.lista_de_links: list = []

    def iniciar_pesquisa(self):

        url = ("https://www.abcdoabc.com.br/Busca?q={}".format(self.termos_da_pesquisa))

        self.driver = webdriver.Firefox()
        self.driver.get(url)

    def capturar_links(self):

        sleep(2)
        noticias = self.driver.find_elements(By.CLASS_NAME, 'gsc-webResult')

        """filtrando a lista para não terem links repetidos"""
        [self.lista_de_links.append(noticia.find_element(By.TAG_NAME, 'a').get_attribute('href'))
         for noticia in noticias if noticia.find_element(By.TAG_NAME, 'a').get_attribute('href') not in self.lista_de_links]

        for link in self.lista_de_links:
            print(link)

        paginas = self.driver.find_elements(By.CLASS_NAME, 'gsc-cursor-page')

        print(len(paginas))
        print("\n")

        """é necessario fechar os anuncios na pagina porque eles atrapalham o acesso as demais paginas"""
        try:
            fechar_anuncio = self.driver.find_element(
                By.ID, "clever-49517-sticky-footer-button")
            fechar_anuncio.click()
        except:
            print("pagina sem anuncio\n")

        try:
            fechar_anuncio = self.driver.find_element(
                By.CLASS_NAME, "lx_close_button")
            fechar_anuncio.click()
        except:
            print("pagina sem anuncio\n")

        # sleep(2)

        """
        Aqui eu estou fazendo um looping com a quantidade de paginas.
        Ao passar para proxima pagina a lista de paginas precisa ser renovada porque os botoes são renovados.
        """
        try:
            for i in range(len(paginas)):

                """é necessario fechar os anuncios na pagina porque eles atrapalham o acesso as demais paginas"""
                try:
                    fechar_anuncio = self.driver.find_element(
                        By.ID, "clever-49517-sticky-footer-button")
                    fechar_anuncio.click()
                except:
                    print("pagina sem anuncio\n")

                try:
                    fechar_anuncio = self.driver.find_element(
                        By.CLASS_NAME, "lx_close_button")
                    fechar_anuncio.click()
                except:
                    print("pagina sem anuncio\n")

                print("Pagina:", (i+1))

                sleep(2)

                paginas = self.driver.find_elements(
                    By.CLASS_NAME, 'gsc-cursor-page')

                pagina = paginas[i]

                """O evento de click so ocorre se o index da pagina for maior que o da pagina atual"""
                if (int(pagina.get_attribute('textContent')) > int(pagina.get_attribute('textContent')) - 1):

                    pagina.click()

                    sleep(2)

                    noticias = self.driver.find_elements(
                        By.CLASS_NAME, 'gsc-webResult')

                    """filtrando a lista para não terem links repetidos"""
                    [self.lista_de_links.append(noticia.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                    for noticia in noticias if noticia.find_element(By.TAG_NAME, 'a').get_attribute('href') not in self.lista_de_links]

                    for link in self.lista_de_links:
                        pass

            print(len(self.lista_de_links))

            self.driver.close()
        except:
            print("pagina sem resultado")

    def raspar_noticia(self):

        profile = webdriver.FirefoxProfile()
        profile.set_preference("javascript.enabled", False)

        self.driver = webdriver.Firefox(profile)

        for link in self.lista_de_links:
            try:
                self.driver.get(link)
                self.criar_arquivo(link)
            except:
                print("erro no metodo raspar_noticia")

        self.driver.close()

    def criar_arquivo(self, link):

        sleep(2)

        import re

        link_sem_caracteres_especiais = re.sub('[^0-9a-zA-Z]+', '_', link)
        print(link_sem_caracteres_especiais)

        data = self.driver.find_element(
            By.CLASS_NAME, "author").get_attribute('textContent')

        if int(data[33:37]) < 2018:
            return
        if int(data[33:37]) > 2021:
            return

        data = self.formatar_data(data)

        titulo = "{}-{}".format(data, link_sem_caracteres_especiais)

        paragrafos = self.driver.find_element(By.TAG_NAME, 'article')

        paragrafos = paragrafos.find_elements(By.TAG_NAME, 'p')

        texto = ''

        for paragrafo in paragrafos:
            print(paragrafo.get_attribute('textContent'), "\n")
            texto = texto + \
                "{}\n".format(paragrafo.get_attribute('textContent'))

        try:
            arquivo = open('{}.txt'.format(titulo), 'w+', encoding="utf-8")
            arquivo.write(texto)
            arquivo.close()
        except:
            try:
                arquivo.close()
            except:
                pass
            print("nao conseguiu criar o arquivo")

        try:
            shutil.move('D:\crawler_abcdoabc\{}.txt'.format(titulo),
                        "D:\crawler_abcdoabc\{}".format(self.termos_da_pesquisa))
        except:
            print("não conseguiu mover para pasta")

    def formatar_data(self, data):

        ano = data[33:37]
        dia = data[27:29]
        mes = data[30:32]

        data = '{}-{}-{}'.format(ano, mes, dia)

        return data
