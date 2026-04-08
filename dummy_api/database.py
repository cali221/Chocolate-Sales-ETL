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
        
    engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}", connect_args={"options": "-c timezone=utc"})
    return engine

def execute_psql_script(path_to_script, conn):
    with open(path_to_script) as file:
        query = text(file.read())
        conn.execute(query)
        conn.commit()

def setup_db(engine):
    print("setup_db called, setting up OLTP database:")

    # create the schema
    print("Create oltp_online_store schema if it doesn't exist...")
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS oltp_online_store"))
        connection.commit()

    # add the tables
    print("Adding the tables...")
    SQLModel.metadata.create_all(engine)

    with engine.connect() as connection:
        sql_scripts_dir = Path(__file__).parent / "sql_scripts"

        # add db triggers
        print("Adding database triggers...")
        execute_psql_script(sql_scripts_dir / "setup_db_triggers.psql", connection)

        # pre-fill the DB
        print("Pre-filling the database")

        # fill countries table
        execute_psql_script(sql_scripts_dir / "prefill_oltp_countries.psql", connection)

        # fill customers table
        execute_psql_script(sql_scripts_dir / "prefill_oltp_customers.psql", connection)

        # fill products table
        execute_psql_script(sql_scripts_dir / "prefill_oltp_products.psql", connection)

        # fill status table
        execute_psql_script(sql_scripts_dir / "prefill_oltp_status.psql", connection)

