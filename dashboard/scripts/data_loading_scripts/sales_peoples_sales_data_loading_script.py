from scripts.utils import fetch_from_db

def load_sales_peoples_sales_data(engine):
    """
    load the sales data attributed to sales people from the database
    (shared between all charts for sales people's sales)
    """
    # get all required data by joining tables
    sql_query = """
                SELECT s.sales_amount_usd,
                       s.boxes_shipped,
                       s.date,
                       c.country_name AS country,
                       sp.sales_person_name AS sales_person,
                       p.product_name AS product
                FROM marts.fct_salespeople_sales s
                JOIN marts.dim_customers_countries c ON c.country_id = s.country_id
                JOIN marts.dim_sales_people sp ON sp.sales_person_id = s.sales_person_id
                JOIN marts.dim_products p on p.product_id = s.product_id
                """
    
    # get dataframe from db's data
    sales_peoples_sales = fetch_from_db(sql_query, engine)

    # raise error if df is empty because it should automatically be filled
    # unlike online store's data
    if sales_peoples_sales.empty:
        raise ValueError("Dataframe for sales people's sales data is empty")

    return sales_peoples_sales