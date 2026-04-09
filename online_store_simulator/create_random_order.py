# python3 create_random_order.py
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
import random
import json

# setup env variable for host (in Docker: database, locally: localhost)
if not os.getenv('USING_DOCKER'):
    print('Not using docker, loading .env.local')
    dotenv_path = Path(__file__).parent.parent / '.env.local'
    load_dotenv(dotenv_path)

host = os.getenv('POSTGRES_HOST')
print(f"host: {host}")

# get product IDs (limit 100)
products = requests.get(f"http://{host}:8000/products").json()
product_ids = [product['id'] for product in products]

# get customer IDs (limit 100)
customers = requests.get(f"http://{host}:8000/customers").json()
customer_ids = [customer['id'] for customer in customers]

# print the available IDs for products and customers
print(f"Product IDs: {product_ids}")
print(f"Customer IDs: {customer_ids}")
print(f"len(product_ids): {len(product_ids)})")

# get a random number of distinct products to order
# should be <= the number of product IDs
number_of_items = random.randint(1, len(product_ids))

# get number_of_items unique product IDs 
selected_product_ids = random.sample(product_ids, number_of_items)

# get a list of the items to order with their quantities
order_items = [ {"quantity": random.randint(1, 500), "product_id": item} for item in selected_product_ids]

# set up the order data
order_data = {
  "customer_id": random.choice(customer_ids),
  "items": order_items,
  "tax_amount": round(random.uniform(1, 15), 3),
  "discount_amount": round(random.uniform(1, 10), 3),
  "shipping_costs_amount": round(random.uniform(1, 15), 3)
}

# create an order
order_created = requests.post(f"http://{host}:8000/orders", json=order_data)

# print the json results of the endpoint
print(f"Inserted order:\n{json.dumps(order_created.json(), indent=2)}")