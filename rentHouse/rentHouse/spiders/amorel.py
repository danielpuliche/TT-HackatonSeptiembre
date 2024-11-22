import scrapy
import re

class AmorelSpider(scrapy.Spider):
    name = "amorel"
    allowed_domains = ["amorelpasto.com"]
    start_urls = [f'https://amorelpasto.com/clasificados/web/app.php/resultados/Finca%20Raiz/apartamentos%20arriendo?pagina={i}' for i in range(1,11)]

    def parse(self, response):
        DivsItemList = response.css('div[class*="item-list"]')

        for div in DivsItemList:

            detailsDiv = div.css('div.add-details')
            enlace = detailsDiv.css('a::attr(href)').get()

            if enlace is not None:
                enlace = enlace.replace(' ',"%20")
                url_completa = response.urljoin(enlace)
                pagina = response.url.split('pagina=')[-1]
                yield scrapy.Request(url_completa, callback=self.parse_detail, meta={'pagina':pagina})
    
    def parse_detail(self, response):
        newDetailsDiv = response.css('div[class*="ads-details-info"]')

        details = newDetailsDiv.css('h4::text').getall()

        yield{
            'pagina':response.meta.get('pagina'),
            "details":details,
            "url":response.url
        }