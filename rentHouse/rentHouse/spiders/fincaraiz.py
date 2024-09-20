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
            href = anchor.css('::attr(href)').get() 
            tipo_arriendo = anchor.css('span[class*="lc-title"]::text').get().lower().split(' en')[0]
            # Construir URLs absolutas
            base_url = 'https://www.fincaraiz.com.co'
            absolute_url = base_url + href 
            meta = {
                "ciudad":response.url.split('/')[5],
                "departamento":response.url.split('/')[6],                
                "tipo":"_".join(tipo_arriendo.split())     
            }

            # Seguir las URLs para extraer datos de las páginas detalladas
            yield scrapy.Request(url=absolute_url, callback=self.parse_detail, meta=meta)
    

    def parse_detail(self, response):
        # Extraer datos de la página detallada
        #tipo_inmueble = response.css('div.ant-typography.ant-typography-ellipsis.ant-typography-ellipsis-multiple-line strong::text').get()
        ciudad = response.meta.get('ciudad')
        departamento = response.meta.get('departamento')
        tipo = response.meta.get('tipo') 
        valor_estrato = response.css('div.ant-typography.ant-typography-ellipsis strong::text').get().strip()
        size = response.css('span[class*="ant-typography"]::text').getall()
        size = dividir_size("".join(size))
        price = response.css('span[class*="ant-typography price"]').css('strong::text').get()
        if price is None:
            price = None
        else:
            price = float(price.replace('$', '').replace(',', '').strip())
            #price = price.astype(float)
        admin = response.css('span[class*="ant-typography commonExpenses"]::text').get()
        price_full=0
        if admin == "Incluye Administración":
            price_full = price
        elif admin is None:
            price_full = price
        else:
            # Reemplazar los caracteres no deseados
            admin = float(price.replace('$', '').replace('+', '').replace('administración', '').strip().replace('.', '').replace(',', '.'))
            price_full = price + admin
        # if admin is None:
        #     administracion = None
        # else:
        #     administracion = admin#.split()[2] 
        #     #float(administracion)

        antiguedad = response.css('div.ant-typography strong::text').get()

        # antiguedad_st = antiguedad[6]  # Cambia el índice para obtener otro elemento

        # #<div class="ant-typography ant-typography-ellipsis ant-typography-ellipsis-multiple-line" style="margin: 0px; -webkit-line-clamp: 2;" title="1 a 8 años"><strong>1 a 8 años</strong></div>
        # #<div class="ant-typography ant-typography-ellipsis ant-typography-ellipsis-multiple-line" style="margin: 0px; -webkit-line-clamp: 2;" title="Oficina"><strong>Oficina</strong></div>
        # ##<span class="ant-typography commonExpenses body body-regular body-1 medium">+ $ 250.000 administración</span>
        # ##<div class="ant-space ant-space-horizontal ant-space-align-baseline property-typology-tag property-typology-tag-desktop show-icons"><div class="ant-space-item" style="margin-right:16px"><div class="ant-space ant-space-horizontal ant-space-align-center"><div class="ant-space-item" style="margin-right:8px"><span role="img" style="color:#456787" class="anticon"><svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_793_13665)"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.8 1.48L1.06667  12.1979Z" fill="currentColor"></path></g><defs><clipPath id="clip0_793_13665"><rect width="1em" height="1em"></rect></clipPath></defs></svg></span></div><div class="ant-space-item"><span class="ant-typography ant-typography-ellipsis ant-typography-ellipsis-single-line">1<!-- --> Ambiente</span></div></div></div><div class="ant-space-item" style="margin-right:16px"><div class="ant-space ant-space-horizontal ant-space-align-center"><div class="ant-space-item" style="margin-right:8px"><span role="img" style="color:#456787" class="anticon"><svg width="1em" height="1em" viewBox="0 0 13 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M12.9561 11.4978Z" fill="currentColor"></path></svg></span></div><div class="ant-space-item"><span class="ant-typography ant-typography-ellipsis ant-typography-ellipsis-single-line"> <!-- -->1<!-- --> Baño</span></div></div></div><div class="ant-space-item"><div class="ant-space ant-space-horizontal ant-space-align-center"><div class="ant-space-item" style="margin-right:8px"><span role="img" style="color:#456787" class="anticon"><svg width="1em" height="1em" viewBox="0 0 17 14" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16.17 1.00039C16.223 .13848Z" fill="currentColor"></path></svg></span></div><div class="ant-space-item"><span class="ant-typography ant-typography-ellipsis ant-typography-ellipsis-single-line">34<!-- --> <!-- -->m²</span></div></div></div></div>
        # ##<div class="ant-row ant-row-middle property-price-tag" style="margin-left:-4px;margin-right:-4px"><div style="padding-left:4px;padding-right:4px;display:flex;align-items:center;justify-content:center" class="ant-col"><span class="ant-typography price heading heading-3 high"><strong>$ 850.000</strong></span></div><div style="padding-left:4px;padding-right:4px" class="ant-col ant-col-24"><span class="ant-typography operation_type body body-regular body-1 medium">Precio de<!-- --> <!-- -->Arriendo</span></div><div style="padding-left:4px;padding-right:4px" class="ant-col expenses-col"><span class="ant-typography commonExpenses body body-regular body-1 medium">+ $ 250.000 administración</span></div></div>        

        
        # # Crear el diccionario con los datos extraídos
        yield {
            'url': response.url,
            "ciudad": ciudad,
            "departamento": departamento,
            "tipo":tipo,
            'estrato': valor_estrato,
            "bathrooms": size["bathrooms"],
            "ambientes": size["ambiente"],
            "habitaciones": size["habitaciones"],
            "metros": size["metros"],
            "price": price_full,
            # "administración": administracion, 
            "antiguedad": antiguedad.replace('años', '').strip(),

        }
