import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def load_to_db(df):
    """
    load dataframe to postgresql database titled choco_db
    """
    if not os.getenv('USING_DOCKER'):
        print('Not using docker, loading .env.local')
        dotenv_path = Path(__file__).parent.parent.parent / '.env.local'
        load_dotenv(dotenv_path)

    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

    print("Loading DataFrame to database...")

    try:
        # automatically rollback if failed, commit if successful
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE kaggle_hist_data.choco_stats"))
            df.to_sql("choco_stats", 
                    conn, 
                    if_exists="append", 
                    index=False, 
                    schema="kaggle_hist_data")
        print("Finished loading dataframe into database")
    except Exception as e:
        print(f"Failed to load dataframe into DB: {e}")