"""
Product

api_call - potrzeba zmiany danych w Shoper

"""

class Product:
    def __init__(self, product_code, stock, id = 0, api_call = 1):
        self.product_code = product_code
        self.stock = stock
        self.id = id  
        self.api_call = api_call

    def __str__(self):
        return f"{self.id},{self.product_code},{self.stock} \n"
    
    def save(self):
        return f"{self.id},{self.product_code},{self.stock} \n"

    def id_isSet(self):
        if self.id == 0:
            return True
        else: 
            return False
        
    def id_set(self, value):
        self.id = value
        
    def productStock_set(self, stockNew):
        if self.stock != stockNew:
            return True
        else:
            return False
