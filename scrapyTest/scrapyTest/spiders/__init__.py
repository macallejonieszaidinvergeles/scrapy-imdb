import scrapy

from urllib.parse import urljoin

contador = 0

class QuotesSpider(scrapy.Spider):
    name = "scrapyTest"
    # Nombre de dominio del sitio web rastreado
    allowed_domains = ["imdb.com"]
    # Página de inicio de la página de rastreo
    start_urls = [
        "https://www.imdb.com/search/title/?genres=comedy&title_type=feature&explore=genres",
    ]

    def parse(self, response):
        global contador

        links = response.css(
            "div.lister-item-content>h3.lister-item-header  a::attr(href)"
        ).extract()
        
        next = response.css(
            "#main > div > div.desc > a.lister-page-next.next-page::attr(href)"
        ).extract()
        
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
        # print("-------next--------")
        # print(next_final)

        print(f"contador:{contador}")

        if contador < 2:
            if next:
                contador += 1
                yield scrapy.Request(next_final, callback=self.parse)

    def reseñas(self, response):
        try:
            titulo = response.css("#__next > main > div > section.ipc-page-background.ipc-page-background--base.MainDetailPageLayout__StyledPageBackground-sc-13rp3wh-0.hsughJ > section > div:nth-child(4) > section > section > div.TitleBlock__Container-sc-1nlhx7j-0.hglRHk > div.TitleBlock__TitleContainer-sc-1nlhx7j-1.jxsVNt > h1::text").getall()
        except IndexError:
            titulo = "Not Available"

        try:
            year = response.css(
                "#__next > main > div > section.ipc-page-background.ipc-page-background--base.MainDetailPageLayout__StyledPageBackground-sc-13rp3wh-0.hsughJ > section > div:nth-child(4) > section > section > div.TitleBlock__Container-sc-1nlhx7j-0.hglRHk > div.TitleBlock__TitleContainer-sc-1nlhx7j-1.jxsVNt > div.TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2.hWHMKr > ul > li:nth-child(1) > a::text"
            ).getall()
        except IndexError:
            year = "Not Available"

        try:
            reseñas_usuarios = response.css(
                "li.jxsVNt>a.ipc-link--baseAlt:link, .ipc-link--baseAlt>span.three-Elements span.score::text"
            ).getall()[0]
        except IndexError:
            reseñas_usuarios = "NaN"

        try:
            reseñas_criticos = response.css(
                "li.jxsVNt>a.ipc-link--baseAlt:link, .ipc-link--baseAlt>span.three-Elements span.score::text"
            ).getall()[1]
        except IndexError:
            reseñas_criticos = "NaN"

        try:
            metapuntuación = response.css("span.score-meta::text").getall()
        except IndexError:
            metapuntuación = "NaN"

        try:
            popularidad = response.css(
                "#__next > main > div > section.ipc-page-background.ipc-page-background--base.MainDetailPageLayout__StyledPageBackground-sc-13rp3wh-0.hsughJ > section > div:nth-child(4) > section > section > div.TitleBlock__Container-sc-1nlhx7j-0.hglRHk > div.RatingBar__RatingContainer-sc-85l9wd-0.hNqCJh.TitleBlock__HideableRatingBar-sc-1nlhx7j-4.bhTVMj > div > div:nth-child(3) > a > div > div > div.TrendingButton__ContentWrap-sc-bb3vt8-0.jQthUT > div.TrendingButton__TrendingScore-sc-bb3vt8-1.efbXIW::text"
            ).getall()
        except IndexError:
            popularidad = "Not Available"

        yield {
            "titulo": titulo,
            "año": year,
            "reseñas_usuarios": reseñas_usuarios,
            "reseñas_criticos": reseñas_criticos,
            "metapuntuación": metapuntuación,
            "popularidad": popularidad,
        }
