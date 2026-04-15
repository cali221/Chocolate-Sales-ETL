from shared.oltp_db_models import (Product, 
                                   Country, 
                                   Customer, 
                                   Status, 
                                   Order,
                                   OrderItem)
from sqlmodel import SQLModel

def create_oltp_tables(engine):
    """
    create the tables for the online store schema
    """
    print('Creating tables for oltp_online_store schema...')
    SQLModel.metadata.create_all(engine)
    print('Finished creating tables for oltp_online_store schema')