import scrapy
# from urllib.parse import urlparse
from urllib.parse import urljoin
# from flask import Request


class QuotesSpider(scrapy.Spider):
    name = "scrapyTest"
    # Nombre de dominio del sitio web rastreado
    allowed_domains = ['imdb.com']
    # Página de inicio de la página de rastreo
    start_urls = [
        'https://www.imdb.com/search/title/?genres=comedy&title_type=feature&explore=genres',
    ]

    def parse(self, response):

        # css ('div.content p :: text') Use las Herramientas para desarrolladores de Google Chrome para verificar la ubicación específica del texto que se debe rastrear
        titulos = response.css('div.lister-item-content>h3.lister-item-header a::text').getall()
        links = response.css('div.lister-item-content>h3.lister-item-header  a::attr(href)').extract()
        # links = urljoin('https://www.imdb.com',links)
        next = response.css('div.desc a::attr(href)').extract()
        # next_page = response.css('.next a').attrib['href']

        links_completos = []
        for link in links:
            base_url = "https://www.imdb.com"
            final_url = urljoin(base_url, link)
            # print("----links----")
            links_completos.append(final_url)

        base_url = "https://www.imdb.com"
        next_final = urljoin(base_url, str(next[0]))
        print("-------next--------")
        print(next_final)
        # print("linkk")
        # print(links_completos[0])

        # for link_completo in links_completos:
        #  url = link_completo

        dic = {}
        dic = dict(zip(titulos, links_completos))

        yield dic  # dic

        # Lea el contenido de la página siguiente y vuelva a llamar al método de análisis
        # for a in next_final:

        
        yield scrapy.Request(next_final, callback=self.title)


    def title(self, response):
        # css ('div.content p :: text') Use las Herramientas para desarrolladores de Google Chrome para verificar la ubicación específica del texto que se debe rastrear
        titulos = response.css('div.lister-item-content>h3.lister-item-header a::text').getall()
        links = response.css('div.lister-item-content>h3.lister-item-header  a::attr(href)').extract()
        # links = urljoin('https://www.imdb.com',links)
        next = response.css('div.desc a::attr(href)').extract()
        # next_page = response.css('.next a').attrib['href']

        links_completos = []
        for link in links:
            base_url = "https://www.imdb.com"
            final_url = urljoin(base_url, link)
            # print("----links----")
            links_completos.append(final_url)

        base_url = "https://www.imdb.com"
        next_final = urljoin(base_url, str(next[0]))
        print("-------next--------")
        print(next_final)
        # print("linkk")
        # print(links_completos[0])

        # for link_completo in links_completos:
        #  url = link_completo

        dic = {}
        dic = dict(zip(titulos, links_completos))

        yield dic  # dic

        

    
