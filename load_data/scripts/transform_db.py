import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

def get_psycopg2_conn():
    """
    get connection to PostgreSQL database for psycopg
    """
    if not os.getenv('USING_DOCKER'):
        print('Not using docker, loading .env')
        dotenv_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(dotenv_path)

    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')

    print("Trying to connect to database to transform schema...")
    connection = psycopg2.connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    print("Connected to database")

    return connection

def transform_db_schema(cursor, path_to_script):
    """
    execute psql script to transform schema
    """
    psql_setup_file = open(path_to_script,'r')
    cursor.execute(psql_setup_file.read())

def run_tests(cursor, path_to_script):
    """
    execute psql script to run checks for transformed schema
    """
    with open(path_to_script, 'r') as file:
        file_content_str = file.read()

    queries_arr = [q.strip() for q in file_content_str.strip().split(';') if q.strip()]

    for q in queries_arr:
        print("--------------- QUERY ------------------")
        print(q)
        print("\n")
        print("--------------- RESULT -----------------")
        cursor.execute(q)
        results = cursor.fetchone()[0]
        print(results)
        print("----------------------------------------\n\n")

def transform_and_check(path_to_setup_script, path_to_tests_script):
    """
    connect to PostgreSQL database for psycopg, 
    transform schema and run checks
    """
    try:
        # connect to database
        connection = get_psycopg2_conn()
        cursor = connection.cursor()

        # transform database
        print("Transforming database schema...")
        transform_db_schema(cursor, path_to_setup_script)
        connection.commit()
        print("Finished transforming database schema")

        # check
        print("Running checks for transformed schema...")
        run_tests(cursor, path_to_tests_script)
        print("Finished running checks")
    except Exception as e: 
        print(e)
    finally:
        cursor.close()
        connection.close()