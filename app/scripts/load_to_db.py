import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

def load_to_db(df):
    """
    load dataframe to postgresql database titled choco_db
    """
    load_dotenv()
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

    print("Loading DataFrame to database...")
    df.to_sql("choco_stats", engine, if_exists="replace", index=False)
    print("Finished loading dataframe into database")