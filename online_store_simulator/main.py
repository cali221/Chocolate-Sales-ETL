# python -m main
import os
import time
import random
from pathlib import Path
from dotenv import load_dotenv
from scripts.create_random_order import create_random_order
from scripts.update_random_orders import update_random_orders_status

# set up  host
if not os.getenv('USING_DOCKER'):
    print('Not using docker, loading .env.local')
    dotenv_path = Path(__file__).parent.parent / '.env.local'
    load_dotenv(dotenv_path)

host = os.getenv('API_HOST')
port = os.getenv('API_PORT')
print(f"host: {host}, port: {port}")

while True:
    # simulate random events in the online store with pauses:
    # create one random order
    create_random_order(host, port)
    time.sleep(random.randint(2, 5))

    # update one or more orders' status
    update_random_orders_status(host, port)
    time.sleep(random.randint(2, 5))
