# python -m main
import os
from pathlib import Path
from dotenv import load_dotenv
from scripts.create_random_order import create_random_order
from scripts.update_random_orders import update_random_orders_status

if not os.getenv('USING_DOCKER'):
    print('Not using docker, loading .env.local')
    dotenv_path = Path(__file__).parent.parent / '.env.local'
    load_dotenv(dotenv_path)

host = os.getenv('POSTGRES_HOST')
print(f"host: {host}")

create_random_order(host)
update_random_orders_status(host)

