#!/usr/bin/python
import json, os
import pytesseract
from PIL import Image
from requests_html import HTMLSession,requests
session = HTMLSession()


domain = 'https://www.edu.xunta.es'
# center detail endpoint.
url = 'https://www.edu.xunta.es/centroseducativos/CargarDetalleCentro.do?codigo='


def init():
    
    print('Starting...')
    f = open('centros.json')
    centers = json.load(f)
    with open('emails', 'a') as emails:
        for center in centers:
            if 'A Coru' in center['label'] and 'IES' in center['label']: # TODO modify filter.
                id = center['codigo']
                r = session.get(url + id)
                print('Retrieving center id ' + id + ' email information...')
                r = requests.get(domain + r.html.search('img src="{}"')[0])
                with open(id + '.png', 'wb') as f:
                    f.write(r.content)
                # Image recognition
                image = Image.open(id + '.png')
                email = pytesseract.image_to_string(image, lang='eng')
                emails.write(email)
                
    os.system('rm *.png')
    print('Finished, results at: "emails" file')
            

if __name__ == "__main__" :
     init()  