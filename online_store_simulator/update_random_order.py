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

# get order IDs
orders = requests.get(f"http://{host}:8000/orders").json()
order_ids = [order['id'] for order in orders]