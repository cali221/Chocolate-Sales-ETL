from db_setup.utils.get_engine import get_engine
from db_setup.scripts.create_schemas import create_schemas
from db_setup.scripts.create_tables import create_oltp_tables
from db_setup.scripts.create_tables import create_kaggle_data_table
from db_setup.scripts.add_db_triggers import add_oltp_db_triggers
from db_setup.scripts.prefill_oltp_tables import prefill_oltp_tables

engine = get_engine()

with engine.connect() as connection:
    create_schemas(connection)
    create_kaggle_data_table(connection)
    create_oltp_tables(engine)
    add_oltp_db_triggers(connection)
    prefill_oltp_tables(connection)
    

