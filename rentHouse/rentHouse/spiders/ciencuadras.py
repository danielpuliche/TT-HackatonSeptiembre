import scrapy


class CiencuadrasSpider(scrapy.Spider):
    name = "ciencuadras"
    allowed_domains = ["www.ciencuadras.com"]
    start_urls = [f'https://www.ciencuadras.com/arriendo/popayan?q=Popay%C3%A1n']

    def parse(self, response):
        divWrapper = response.css('div[class*="container-list-card"]').get()

        yield {
            "div":divWrapper
        }

        # AnchorsTarjetasArriendo = sectionWrapper.css('a[class*="lc-data"]')

        # for anchor in AnchorsTarjetasArriendo:
        #     price = anchor.css('div.lc-price').css('strong::text').get()
        #     size = anchor.css('div.lc-typologyTag').css('strong::text').getall()
        #     tipo_arriendo = anchor.css('span[class*="lc-title"]::text').get().lower().split(' en')[0]

        #     size = dividir_size("".join(size))

        #     yield {
        #         "ciudad":response.url.split('/')[5],
        #         "departamento":response.url.split('/')[6],                
        #         "tipo":"_".join(tipo_arriendo.split()),
        #         "bathrooms":size["bathrooms"],
        #         "ambientes":size["ambiente"],
        #         "habitaciones":size["habitaciones"],
        #         "metros":size["metros"],
        #         "price":float(price.replace('$', '').replace(',', '').strip())     
        #     }
