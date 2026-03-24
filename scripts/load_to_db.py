import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

def load_to_db(df):
    """
    load dataframe to postgresql database titled choco_db
    """
    load_dotenv()
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PORT = os.getenv('DB_PORT')
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/choco_db")

    print(".................... loading dataframe into database ......................")
    df.to_sql("choco_stats", engine, if_exists="replace", index=False)
    print(".................... finished loading dataframe into database ......................")