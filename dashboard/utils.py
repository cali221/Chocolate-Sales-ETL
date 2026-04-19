from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from pathlib import Path
import pandas as pd

def get_engine():
    if not os.getenv('USING_DOCKER'):
        print('Not using docker, loading .env.local')
        dotenv_path = Path(__file__).parent.parent / '.env.local'
        load_dotenv(dotenv_path)

    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    return engine

def validate_time_range_and_filter(time_range_arr, df_to_filter, date_col_name):
    if len(time_range_arr) == 2:
        filtered_df = df_to_filter[df_to_filter[date_col_name].between(time_range_arr[0], 
                                                                       time_range_arr[1])]
        return filtered_df, None
    else:
        return None, "Invalid date range. Please pick one start date and one end date"

