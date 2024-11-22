import requests
import csv
import unicodedata
import numpy as np

def quitar_tildes(cadena):
	cadena_normalizada = unicodedata.normalize('NFD', cadena)

	cadena_sin_tildes = ''.join(c for c in cadena_normalizada if unicodedata.category(c) != 'Mn')

	return cadena_sin_tildes

def makePost(data):

	url = f'https://search-service.fincaraiz.com.co/api/v1/properties/search'

	response = requests.post(url, json=data)

	resultado = None
	if response.status_code == 200:
		resultado = response.json()
	else:
		print(f'Error en la solicitud: {response.status_code}')
	
	return resultado

def getDataArriendo(resultado,ciudad,departamento):
	results = resultado['hits']['hits']
	arriendos = []
	for r in results:
		arriendoObj = r['_source']['listing']
		technicalSheet = arriendoObj.get('technicalSheet')
	
		arriendo = {
			'estrato':arriendoObj.get('stratum'),
			'url':"https://www.fincaraiz.com.co"+arriendoObj.get('link'),
			'tipo':quitar_tildes(technicalSheet[1].get('value').lower().replace(' ','_')),
			'baths':technicalSheet[3].get('value'),
			'rooms':technicalSheet[7].get('value'),
			'area':arriendoObj.get('m2'),
			'precio':arriendoObj.get('price').get('admin_included'),
			'antiguedad':technicalSheet[6].get('value'),
			'ciudad':ciudad,
			'departamento':departamento,
			'lat':arriendoObj.get('latitude'),
			'long':arriendoObj.get('longitude'),
		}
		arriendos.append(arriendo)
	return arriendos

archivo_csv = 'fincaraiz.csv'

dataPopayan = {
    "variables": {
        "rows": 100,
        "params": {
            "page": 1,
            "order": 2,
            "operation_type_id": 2,
            "currencyID": 4,
            "m2Currency": 4,
            "locations": [
                {
                    "country": [
                        {
                            "name": "Colombia",
                            "id": "858656c1-bbb1-4b0d-b569-f61bbdebc8f0",
                            "slug": "country-48-colombia"
                        }
                    ],
                    "name": "Popayán",
                    "location_point": {
                        "coordinates": [
                            -76.59778778530963,
                            2.4598871092834242
                        ],
                        "type": "point"
                    },
                    "id": "7d9ce441-b5f8-4db4-a1a6-feb317771752",
                    "type": "CITY",
                    "slug": [
                        "city-colombia-19-001"
                    ],
                    "estate": {
                        "name": "Cauca",
                        "id": "a4f7acee-01dc-4d5d-9f3d-d34889813a16",
                        "slug": "state-colombia-19-cauca"
                    },
                    "label": "Popayán <br/><span style='font-size:12px'>Cauca</span>"
                }
            ]
        },
        "page": 1,
        "source": 10
    },
    "query": ""
}
dataArmenia = {
    "variables": {
        "rows": 900,
        "params": {
            "page": 1,
            "order": 2,
            "operation_type_id": 2,
            "locations": [
                {
                    "country": [
                        {
                            "name": "Colombia",
                            "id": "858656c1-bbb1-4b0d-b569-f61bbdebc8f0",
                            "slug": "country-48-colombia"
                        }
                    ],
                    "name": "Armenia",
                    "location_point": {
                        "coordinates": [
                            -75.68052950793465,
                            4.535830266737521
                        ],
                        "type": "point"
                    },
                    "id": "0f4c7911-6b55-4242-9c67-4226b7478fa0",
                    "type": "CITY",
                    "slug": [
                        "city-colombia-63-001"
                    ],
                    "estate": {
                        "name": "Quindio",
                        "id": "209f5ed2-e25b-4039-ad3c-ae18bfceb1a1",
                        "slug": "state-colombia-63-quindio"
                    },
                    "label": "Armenia <br/><span style='font-size:12px'>Quindio</span>"
                }
            ],
            "currencyID": 4,
            "m2Currency": 4
        },
        "page": 1,
        "source": 10
    },
    "query": ""
}
dataValledupar = {
    "variables": {
        "rows": 200,
        "params": {
            "page": 1,
            "order": 2,
            "operation_type_id": 2,
            "locations": [
                {
                    "country": [
                        {
                            "name": "Colombia",
                            "id": "858656c1-bbb1-4b0d-b569-f61bbdebc8f0",
                            "slug": "country-48-colombia"
                        }
                    ],
                    "name": "Valledupar",
                    "location_point": {
                        "coordinates": [
                            -73.258740547,
                            10.464451867
                        ],
                        "type": "point"
                    },
                    "id": "ef8b63aa-09f8-4ae4-bdfe-6f36ca178d4b",
                    "type": "CITY",
                    "slug": [
                        "city-colombia-20-001"
                    ],
                    "estate": {
                        "name": "Cesar",
                        "id": "e2c9ed05-5149-49d1-a5bb-a5110b36c04c",
                        "slug": "state-colombia-20-cesar"
                    },
                    "label": "Valledupar <br/><span style='font-size:12px'>Cesar</span>"
                }
            ],
            "currencyID": 4,
            "m2Currency": 4
        },
        "page": 1,
        "source": 10
    },
    "query": ""
}
dataBucaramanga = {
    "variables": {
        "rows": 3200,
        "params": {
            "page": 1,
            "order": 2,
            "operation_type_id": 2,
            "locations": [
                {
                    "country": [
                        {
                            "name": "Colombia",
                            "id": "858656c1-bbb1-4b0d-b569-f61bbdebc8f0",
                            "slug": "country-48-colombia"
                        }
                    ],
                    "name": "Bucaramanga",
                    "location_point": {
                        "coordinates": [
                            -73.12898235739321,
                            7.119264837091706
                        ],
                        "type": "point"
                    },
                    "id": "9315523c-12cc-4678-804d-d05e4cf174b4",
                    "type": "CITY",
                    "slug": [
                        "city-colombia-68-001"
                    ],
                    "estate": {
                        "name": "Santander",
                        "id": "6899b232-a482-4fc7-98f8-21aa670bf4c1",
                        "slug": "state-colombia-68-santander"
                    },
                    "label": "Bucaramanga <br/><span style='font-size:12px'>Santander</span>"
                }
            ],
            "currencyID": 4,
            "m2Currency": 4
        },
        "page": 1,
        "source": 10
    },
    "query": ""
}

resultadoPop = makePost(dataPopayan)
arriendosPop = getDataArriendo(resultadoPop,'popayan','cauca') if resultadoPop is not None else None

resultadoArm = makePost(dataArmenia)
arriendosArm = getDataArriendo(resultadoArm,'armenia','quindio') if resultadoArm is not None else None

resultadoVall = makePost(dataValledupar)
arriendosVall = getDataArriendo(resultadoVall,'valledupar','cesar') if resultadoVall is not None else None

resultadoBuc = makePost(dataBucaramanga)
arriendosBuc = getDataArriendo(resultadoBuc,'bucaramanga','santander') if resultadoBuc is not None else None

arriendos = np.concatenate((arriendosPop, arriendosArm, arriendosVall, arriendosBuc), axis=0)
with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
	escritor = csv.DictWriter(archivo, fieldnames=['estrato','url','tipo','baths','rooms','area','precio','antiguedad','ciudad','departamento','lat','long'])
	escritor.writeheader()
	escritor.writerows(arriendos)