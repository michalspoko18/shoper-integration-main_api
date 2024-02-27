import xml.etree.ElementTree as ET
import requests
import classes.product as product
import functions.api as functions
import csv
import os

def products_get(url_prod, products):
    try:
        if os.path.exists("products.csv") and os.path.getsize("products.csv") != 0:
            with open("products.csv", mode='r') as prodcsv:
                reader = csv.DictReader(prodcsv)
                rows = list(reader)
                
                for row in rows:        
                    print(row['product_code'])
                    if int(row['product_id']) != 0:
                        product_code = row['product_code']
                        id = row['product_id']
                        stock = row['stock']
                        products[row['product_code']] = product.Product(product_code, stock, id)
            return 0 

        response_xml = requests.get(url_prod)
        root = ET.fromstring(response_xml.content)

        #x = 1

        for produkt_xml in root.findall('.//offers//offer'):
            #if x > 100: return 0
            product_code = int(produkt_xml.find('id').text)
            stock = int(produkt_xml.find('onstock').text)

            products[product_code] = product.Product(product_code, stock)
            #x+=1
        

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def set_product_id(products):

    product_codes_to_send = []
    product_codes_to_add = []

    for product_code in products:

        if products[product_code].id_isSet():
            product_codes_to_send.append(product_code)

        else:
           product_codes_to_add.append(product_code) 

        if len(product_codes_to_send) == 25:
            functions.send_bulk_request_for_id(product_codes_to_send, products)
            product_codes_to_send = []

        if len(product_codes_to_add) == 25:
            #send_bulk_request_for_add(product_codes_to_add, products)
            product_codes_to_add = []

    if product_codes_to_send:
        functions.send_bulk_request_for_id(product_codes_to_send, products)
    
    if product_codes_to_add:
        #send_bulk_request_for_add(product_codes_to_add, products)
        product_codes_to_add = []
