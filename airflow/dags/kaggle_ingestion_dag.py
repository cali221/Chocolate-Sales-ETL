from airflow import DAG
from datetime import datetime

default_arguments = {
    'owner': 'me',
    'email': 'theresiacalista57@gmail.com',
    'start_date': datetime(2026, 4, 15)
}

with DAG('load_kaggle_data', default_arguments=default_arguments) as load_kaggle_data_dag:
    