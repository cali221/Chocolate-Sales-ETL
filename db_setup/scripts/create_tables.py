from shared.oltp_db_models import (Product, 
                                   Country, 
                                   Customer, 
                                   Status, 
                                   Order,
                                   OrderItem)
from sqlmodel import SQLModel
from sqlalchemy import text

def create_kaggle_data_table(connection):
    """
    create choco_stats table for Kaggle historical data
    """
    print('Creating choco_stats table for Kaggle data...')
    connection.execute(text("""
                            CREATE TABLE IF NOT EXISTS kaggle_hist_data.choco_stats(
                                "Sales Person" TEXT,
                                "Country" TEXT,
                                "Product" TEXT,
                                "Date" TEXT,
                                "Amount" TEXT,
                                "Boxes Shipped" BIGINT
                            )
                            """))
    connection.commit()
    print('Finished creating choco_stats table')

def create_oltp_tables(engine):
    """
    create the tables for the online store schema
    """
    print('Creating tables for oltp_online_store schema...')
    SQLModel.metadata.create_all(engine)
    print('Finished creating tables for oltp_online_store schema')