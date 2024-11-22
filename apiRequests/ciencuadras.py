import requests
import csv
import unicodedata
import numpy as np

def quitar_tildes(cadena):
	cadena_normalizada = unicodedata.normalize('NFD', cadena)

	cadena_sin_tildes = ''.join(c for c in cadena_normalizada if unicodedata.category(c) != 'Mn')

	return cadena_sin_tildes

def makePost(data):

	url = f'https://api-backend.ciencuadras.com/prod/search-results/v1'

	token = 'eyJraWQiOiJSNDBGb0R1OFRKYVJjYUgzRlhQMzBhZXlvb09LSWgxS2tWUUxHMkZSQlJNPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxdGNtbTczNDJqNjY2MW80NGdnYm80ajE2cCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiY2llbmN1YWRyYXMtcHJvZC1hcGktc2VydmVyXC9yZWFkIGNpZW5jdWFkcmFzLXByb2QtYXBpLXNlcnZlclwvd3JpdGUiLCJhdXRoX3RpbWUiOjE3MjY4NDExNTYsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX1YyWGRBYmJtbiIsImV4cCI6MTcyNjg0NDc1NiwiaWF0IjoxNzI2ODQxMTU2LCJ2ZXJzaW9uIjoyLCJqdGkiOiI3NGY0ZDdmOS0xYTI0LTQzMmUtODZhZC1hOGI5ZGIzYjdhNDciLCJjbGllbnRfaWQiOiIxdGNtbTczNDJqNjY2MW80NGdnYm80ajE2cCJ9.RQZn9E1n0nFQWCBRnxN6fZx5Q9x7xPVPVxMHAIZeT3KZu4Bf8ZgclVoD8Vu4LCSwSKHPzE0DNVr8E5AnpZvv9Xezfs0wAyXc_I9YLBCUy0qAZBe2OosU0QFwxe_ejSjWk9gfXlHopUDs85Cy7i53y11ncQLLimtFKs__HITTT7laqZppOtMiVtMudeEWA6xf8usOvQ-7YGtLXJ_hlUtP2jyOA8xVLicRVtltfR78dEVNhus0sFMNqh_z2KYb81uNz3-XfAU3rNb_Z8qg3UyTtqG8BMZ6CYElv5sKI1qrJuQI1VCer4jGTEFYNaxba7jQUQmhAlBmSJFCfdGiCvHbWw'

	headers = {
		'Authorization':f'Bearer {token}'
	}

	response = requests.post(url, json=data, headers=headers)

	resultado = None
	if response.status_code == 200:
		resultado = response.json()
	else:
		print(f'Error en la solicitud: {response.status_code}')
	
	return resultado

def getDataArriendo(resultado):
	results = resultado['data']['results']
	arriendos = []
	for r in results:
		arriendo = {
			'estrato':r.get('stratum'),
			'url':"https://www.ciencuadras.com/"+r.get('url'),
			'tipo':r.get('realEstateType').lower().replace(' ','_'),
			'baths':r.get('baths'),
			'rooms':r.get('rooms'),
			'area':r.get('area'),
			'precio':r.get('rentPrice'),
			'antiguedad':r.get('antiquity'),
			'ciudad':quitar_tildes(r.get('city').lower()),
			'departamento':r.get('department').lower(),
			'lat':r.get('coordinates').get('latitude'),
			'long':r.get('coordinates').get('longitude')
		}
		# url, tipo, estrato, baths, !ambientes, habitaciones, metros, precio, antiguedad, ciudad, departamento
		arriendos.append(arriendo)
	return arriendos

archivo_csv = 'ciencuadras.csv'

dataPopayan = {
	"from":0,
	"fromNear":0,
	"pathUrl":"/arriendo/popayan",
	"radio":"2km",
	"requestId":"5929c850-a24b-aae9-b723-301d342dbd49",
	"size":20,
	"sizeMap":150,
	"sizeNear":20,
	"transactionType":"arriendo"
}
dataArmenia = {
	"radio": "2km",
	"size": 200,
	"sizeMap": 150,
	"transactionType": "arriendo",
	"fromNear": 0,
	"from": 0,
	"sizeNear": 20,
	"project": False,
	"offer": 0,
	"requestId": "de41649a-60ee-92a2-a80f-105721548987",
	"department": "quindio",
	"city": "armenia",
	"sortOrder": "desc",
	"colombiansAbroad": False,
	"expandSearch": False,
	"hasDevolution": False,
	"generalSearch": "",
	"SeoParamLocation": "Armenia"
}
dataValledupar = {
	"radio": "2km",
	"size": 20,
	"sizeMap": 150,
	"transactionType": "arriendo",
	"pathUrl": "/arriendo/valledupar",
	"fromNear": 0,
	"from": 0,
	"sizeNear": 20,
	"requestId": "94985c76-392a-b3be-9520-1ac94afa32fa"
}
dataBucaramanga = {
    "radio": "2km",
    "size": 1700,
    "sizeMap": 150,
    "transactionType": "arriendo",
    "fromNear": 0,
    "from": 0,
    "sizeNear": 20,
    "project": False,
    "offer": 0,
    "requestId": "be8cf781-af71-b9c7-84da-004d0bf6fafe",
    "department": "santander",
    "city": "bucaramanga",
    "sortOrder": "desc",
    "colombiansAbroad": False,
    "expandSearch": False,
    "hasDevolution": False,
    "generalSearch": "",
    "SeoParamLocation": "Bucaramanga"
}

resultadoPop = makePost(dataPopayan)
resultadoArm = makePost(dataArmenia)
resultadoVall = makePost(dataValledupar)
resultadoBuc = makePost(dataBucaramanga)

arriendosPop = getDataArriendo(resultadoPop) if resultadoPop is not None else None
arriendosArm = getDataArriendo(resultadoArm) if resultadoArm is not None else None
arriendosVall = getDataArriendo(resultadoVall) if resultadoVall is not None else None
arriendosBuc = getDataArriendo(resultadoBuc) if resultadoBuc is not None else None

arriendos = np.concatenate((arriendosPop, arriendosArm, arriendosVall, arriendosBuc), axis=0)
	
with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
	escritor = csv.DictWriter(archivo, fieldnames=['estrato','url','tipo','baths','rooms','area','precio','antiguedad','ciudad','departamento','lat','long'])
	escritor.writeheader()
	escritor.writerows(arriendos)