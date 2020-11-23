#!/usr/bin/python
import json
import os
import pytesseract
from PIL import Image
from requests_html import HTMLSession, requests
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
            label = center['label']
            if 'A Coru' in label and ('IES ' in label or 'CPR ' in label or 'CPI ' in label):
                id = center['codigo']
                try:
                    r = session.get(url + id)
                    image_path = r.html.search('img src="{}"')[0]
                    print('Retrieving center id ' + id + ' email information...')
                    r = requests.get(domain + image_path)
                    with open(id + '.png', 'wb') as f:
                        f.write(r.content)
                    # Image recognition
                    image=Image.open(id + '.png')
                    email=pytesseract.image_to_string(image, lang='eng')
                    emails.write(email)
                except Exception as e:
                    print('Image link not found, skipping center:' + id)

    os.system('rm *.png')
    print('Finished, results at: "emails" file')


if __name__ == "__main__":
    init()
