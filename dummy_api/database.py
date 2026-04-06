from sqlmodel import create_engine, text, SQLModel
import os
from dotenv import load_dotenv
from pathlib import Path

def get_engine():
    if not os.getenv('USING_DOCKER'):
        print('Not using docker, loading .env.local')
        dotenv_path = Path(__file__).parent.parent / '.env.local'
        print(f"env path for api: {dotenv_path}")
        load_dotenv(dotenv_path)

    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
        
    engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    return engine

def setup_db(engine):
    print('setup_db CALLED')
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS oltp_online_store"))
        connection.commit()

    print(SQLModel.metadata.tables.keys())
    SQLModel.metadata.create_all(engine)