import requests
import time
import base64
#import functions.helpers as functions
from icecream import ic 
import os
from dotenv import dotenv_values, set_key

global secret, shared, token

try:
    secret = dotenv_values('.env.secret')
    shared = dotenv_values('.env.shared')
    token = dotenv_values('.env.token')
except:
    print("Brak plików .env")


def postToken():

    try:    
        SHOPER_URL = shared['SHOPER_URL_AUTH']
        CLIENT_ID = secret['CLIENT_ID']
        CLIENT_SECRET = secret['CLIENT_SECRET']

        if token['ACCESS_TOKEN'] != '' and testToken(token['ACCESS_TOKEN']) == True: 
            return token['ACCESS_TOKEN']

        try:
            print(f"{SHOPER_URL}, {CLIENT_ID}, {CLIENT_SECRET}")
            auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
            #auth = f"{CLIENT_ID}:{CLIENT_SECRET}"
            headers = {'Authorization': f'Basic {auth}'}
            response_xml = requests.post(SHOPER_URL, headers=headers)
            print(response_xml.json())
            access_token = f"Bearer {response_xml.json().get('access_token')}"
            set_key('.env.token','ACCESS_TOKEN', str(access_token))
            #print(access_token)
            return access_token
        except requests.RequestException as err:
            print(f'Wystąpił błąd: {err}')
    except:
            print('Brak konfiguracji .env')

def testToken(access_token):
    SHOPER_URL_PROD = shared['SHOPER_URL_PROD']
    headers = {'Authorization': access_token, 'Content-Type': 'application/json'}
    respone = requests.get(SHOPER_URL_PROD, headers=headers)
    result = respone.json()

    if result.get('error') == None or False: return True
    else: return False

def howManyPages():
    SHOPER_URL_PROD = shared['SHOPER_URL_PROD']
    headers = {'Authorization': postToken(), 'Content-Type': 'application/json'}
    respone = requests.get(f"{SHOPER_URL_PROD}?limit=50", headers=headers)
    result = respone.json()

    pages = result.get('pages')
    #print(result)
    return pages
    
def updateData():
    with open('response.csv', mode='w', encoding='utf-8') as file:
        file.write(f"product_id,product_code,stock\n")
        file.close()
    pages = int(howManyPages())
    api_call = []
    for page in range(1, pages + 1):
        api_call.append({
            "id": f"prod-list-{page}",
            "path": "/webapi/rest/products",
            "params": {
                "limit": 50,
                "page": page
            },
            "method": "GET"
        })
        if len(api_call) == 20:
            print('api_call\n')
            with open('request.txt', mode='w') as file:
                file.write(str(api_call))
                file.close()
            exportData(bulkRequest(api_call))
            api_call = []
    if api_call:
        exportData(bulkRequest(api_call))

def bulkRequest(body):
    start_time = time.time()
    print('request\n')
    SHOPER_URL_BULK = shared['SHOPER_URL_BULK']
    headers = {'Authorization': postToken(), 'Content-Type': 'application/json'}
    
    response = requests.post(SHOPER_URL_BULK, headers=headers, json=body)
    end_time = time.time()

    duration = end_time - start_time
    print("Czas trwania: ", duration, "sekundy")
    return response.json()

def exportData(data):
    print('export\n')
    #export = data.get('items')[19].get('body').get('list')[49].get('product_id')
    with open('response.csv', mode='a', encoding="utf-8") as file:
        for item in range(0, 20):
            for list in range(0, 50):
                try:
                    export = data.get('items')[item].get('body').get('list')[list]
                except:
                    print('koniec danych')
                    return 0
                file.write(f"{export.get('product_id')}, {export.get('code')}, {export.get('stock').get('stock')}\n")
        file.close()
    print('done')

updateData()