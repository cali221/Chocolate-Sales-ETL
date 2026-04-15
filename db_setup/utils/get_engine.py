from sqlmodel import create_engine
import os
from dotenv import load_dotenv
from pathlib import Path

def get_engine():
    if not os.getenv('USING_DOCKER'):
        print('Not using docker, loading .env.local')
        dotenv_path = Path(__file__).parent.parent.parent / '.env.local'
        print(f"env path for api: {dotenv_path}")
        load_dotenv(dotenv_path)

    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
        
    engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}", connect_args={"options": "-c timezone=utc"})
    return engine