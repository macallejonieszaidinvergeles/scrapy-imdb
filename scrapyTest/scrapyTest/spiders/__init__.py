import scrapy
# from urllib.parse import urlparse
from urllib.parse import urljoin
# from flask import Request

from random import randint
from time import sleep


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
        titulos = response.css(
            'div.lister-item-content>h3.lister-item-header a::text').getall()
        links = response.css(
            'div.lister-item-content>h3.lister-item-header  a::attr(href)').extract()
        # links = urljoin('https://www.imdb.com',links)
        next = response.css('#main > div > div.desc > a.lister-page-next.next-page::attr(href)').extract()
        # next_page = response.css('.next a').attrib['href']

        links_completos = []
        for link in links:
            base_url = "https://www.imdb.com"
            final_url = urljoin(base_url, link)
            # print("----links----")
            links_completos.append(final_url)

        for link_completo in links_completos:
            # print(link_completo)
            yield scrapy.Request(link_completo, callback=self.reseñas)

        base_url = "https://www.imdb.com"
        next_final = urljoin(base_url, str(next[0]))
        print("-------next--------")
        print(next_final)

        if next:
            yield scrapy.Request(next_final, callback=self.parse)
            

    def reseñas(self, response):
        # titulo = []
        # reseñas_usuarios = []
        # reseñas_criticos = []
        # metapuntuación = []

        try:
            titulo = response.css('div.jxsVNt h1::text').getall()
            reseñas_usuarios = response.css(
                'li.jxsVNt>a.ipc-link--baseAlt:link, .ipc-link--baseAlt>span.three-Elements span.score::text').getall()[0]
            reseñas_criticos = response.css(
                'li.jxsVNt>a.ipc-link--baseAlt:link, .ipc-link--baseAlt>span.three-Elements span.score::text').getall()[1]
            metapuntuación = response.css(
                'span.score-meta::text').getall()

        except IndexError:
            titulo = "Not Available"
            reseñas_usuarios = "Not Available"
            reseñas_criticos = "Not Available"
            metapuntuación = "Not Available"

        yield {
            'titulo': titulo,
            'reseñas_usuarios': reseñas_usuarios,
            'reseñas_criticos': reseñas_criticos,
            'metapuntuación': metapuntuación,
        }
