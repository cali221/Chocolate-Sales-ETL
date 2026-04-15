from sqlalchemy import text

def create_schemas(connection):
    """
    Create the required schemas for both kaggle data and online store data
    """
    # create schema for kaggle data 
    print('Creating kaggle_hist_data schema...')
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS kaggle_hist_data"))
    print('Done')

    # create schema for OLTP online store 
    print('Creating oltp_online_store schema...')
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS oltp_online_store"))
    print('Done')
    connection.commit()
