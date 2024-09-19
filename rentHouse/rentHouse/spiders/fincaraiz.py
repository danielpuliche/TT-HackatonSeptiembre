import scrapy
import re

def dividir_size(cadena):
    habitaciones = re.search(r'(\d+)\s*Habs?', cadena)
    bathrooms = re.search(r'(\d+)\s*(Baño|Baños)', cadena)
    metros = re.search(r'(\d+)\s*m²', cadena)
    ambientes = re.search(r'(\d+)\s*Ambiente?', cadena)

    # Extraer los valores encontrados
    habitaciones = float(habitaciones.group(1)) if habitaciones else None
    bathrooms = float(bathrooms.group(1)) if bathrooms else None
    metros = float(metros.group(1)) if metros else None
    ambientes = float(ambientes.group(1)) if ambientes else None

    # Crear y devolver el diccionario
    return {
        'habitaciones': habitaciones,
        'ambiente': ambientes,
        'bathrooms': bathrooms,
        'metros': metros
    }

class FincaraizSpider(scrapy.Spider):
    name = "fincaraiz"
    allowed_domains = ["www.fincaraiz.com.co"]
    ciudades = ["popayan/cauca","armenia/quindio","valledupar/cesar","bucaramanga/santander"]
    start_urls = [f'https://www.fincaraiz.com.co/arriendo/inmuebles/{ciudad}/pagina{i}' for ciudad in ciudades for i in range(1, 11)]

    def parse(self, response):
        sectionWrapper = response.css('section.listingsWrapper')

        AnchorsTarjetasArriendo = sectionWrapper.css('a[class*="lc-data"]')

        for anchor in AnchorsTarjetasArriendo:
            price = anchor.css('div.lc-price').css('strong::text').get()
            size = anchor.css('div.lc-typologyTag').css('strong::text').getall()
            tipo_arriendo = anchor.css('span[class*="lc-title"]::text').get().lower().split(' en')[0]

            size = dividir_size("".join(size))

            yield {
                "ciudad":response.url.split('/')[5],
                "departamento":response.url.split('/')[6],                
                "tipo":"_".join(tipo_arriendo.split()),
                "bathrooms":size["bathrooms"],
                "ambientes":size["ambiente"],
                "habitaciones":size["habitaciones"],
                "metros":size["metros"],
                "price":float(price.replace('$', '').replace(',', '').strip())     
            }
