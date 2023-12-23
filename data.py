import requests
import random
from datetime import datetime, timedelta
from main import Purchase
from connection import session

base_url = "http://127.0.0.1:8000"

def create_product(product_data):
    url = f"{base_url}/products/"
    response = requests.post(url, json=product_data)
    return response.json()

def create_buyer(buyer_data):
    url = f"{base_url}/buyers/"
    response = requests.post(url, json=buyer_data)
    return response.json()

def create_purchase(purchase_data):
    url = f"{base_url}/purchases/"
    response = requests.post(url, json=purchase_data)
    return response.json()

for _ in range(10):
    product_data = {
        "product_name": f"Product {random.randint(1, 100)}",
        "manufacturer": f"Manufacturer {random.randint(1, 100)}",
        "units_of_measurement": random.randint(1, 100),
    }
    create_product(product_data)

for _ in range(5):
    buyer_data = {
        "name": f"Buyer {random.randint(1, 100)}",
        "address": f"Address {random.randint(1, 100)}",
        "phone": f"Phone {random.randint(1, 100)}",
        "contact_person": f"Contact Person {random.randint(1, 100)}",
    }
    create_buyer(buyer_data)

for _ in range(20):
    purchase_data = {
        "product_id": int(random.randint(1, 10)),
        "buyer_id": int(random.randint(1, 5)),
        "delivery_date": (datetime.now() + timedelta(days=random.randint(1, 30))).date().isoformat(),
        "unit_price": int(random.randint(10, 100)),
        "quantity": int(random.randint(1, 10)),
    }
    
    existing_purchase = session.query(Purchase).filter_by(
        product_id=purchase_data["product_id"],
        buyer_id=purchase_data["buyer_id"]
    ).first()

    if existing_purchase is None:
        create_purchase(purchase_data)
    else:
        print(f"Purchase with product_id={purchase_data['product_id']} and buyer_id={purchase_data['buyer_id']} already exists.")

