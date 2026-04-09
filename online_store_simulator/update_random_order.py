# python3 update_random_order.py
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
import random

if not os.getenv('USING_DOCKER'):
    print('Not using docker, loading .env.local')
    dotenv_path = Path(__file__).parent.parent / '.env.local'
    load_dotenv(dotenv_path)

host = os.getenv('POSTGRES_HOST')
print(f"host: {host}")

# get uncompleted order IDs (limit 100)
orders = requests.get(f"http://{host}:8000/uncompleted_orders").json()
order_ids = [order['id'] for order in orders]

# print the available orders
print(f"Order IDs: {order_ids}")

if len(order_ids) != 0:
    print("Uncompleted order found")

    # get a random number of distinct orders to update
    # should be <= the number of order IDs
    number_of_order_to_update = random.randint(1, len(order_ids))
    print(f"Number of orders to update: {number_of_order_to_update}")

    # get number_of_items unique product IDs 
    selected_order_ids = random.sample(order_ids, number_of_order_to_update)
    print(f"Selected order IDs to update: {selected_order_ids}")

    

else:
    print("Uncompleted order not found")