import psycopg2
import os
from dotenv import load_dotenv

def connect_to_db():
    try:
        load_dotenv()
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_HOST = os.getenv('DB_HOST')
        DB_USER = os.getenv('DB_USER')
        DB_PORT = os.getenv('DB_PORT')

        print("Trying to connect to database to transform schema...")
        connection = psycopg2.connect(
            database="choco_db",
            user=DB_USER ,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT ,
        )
        print("Connected to database")

        return connection
    except:
        print("Unable to connect to database")

def transform_db_schema(path_to_script):
    connection = connect_to_db()
    cursor = connection.cursor()
    psql_setup_file = open(path_to_script,'r')

    print("Transforming database schema...")
    cursor.execute(psql_setup_file.read())
    connection.commit()
    print("Finished transforming database schema")
    connection.close()