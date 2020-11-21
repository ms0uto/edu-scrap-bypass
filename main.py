import requests, json
from lxml import etree
import time

# center detail endpoint.
url = 'https://www.edu.xunta.es/centroseducativos/CargarDetalleCentro.do?codigo='


def init():
    
    print('Starting...')
    f = open('centros.json')
    centers = json.load(f)
    for center in centers:
        if 'A Coru' in center['label'] and 'IES' in center['label']: # TODO modify filter.
            # print('Requesting center with id: ' + center['codigo'])
            r = requests.get(url + center['codigo'])
            print(etree.Element(r.text))
            time.sleep(5.0)
            

if __name__ == "__main__" :
     init()  