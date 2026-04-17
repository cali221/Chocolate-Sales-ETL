import streamlit as st
import pandas as pd
import altair as alt
from utils import get_engine
from sales_people_sales_charts import *

def load_sales_peoples_sales_data():
    """
    load the sales data from the database
    """
    engine = get_engine()

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
    sales_peoples_sales = pd.read_sql(sql_query, engine)
    return sales_peoples_sales

def create_dashboard(): 
    """
    create the dashboard showing charts about the data
    """   
    try:
        # get data
        sales_peoples_sales = load_sales_peoples_sales_data()

        # dashboard's title
        st.title("Chocolate Sales by Sales People Between 2022 to 2024")

        # charts about boxes shipped overall:
        # chart for comparing total boxes shipped between countries
        st.subheader("Comparison of total chocolate boxes shipped between countries")
        draw_pie_chart_for_boxes_shipped_per_country(sales_peoples_sales)
       
        # chart for showing the number of boxes shipped over time
        st.subheader("Chocolate boxes shipped over time")
        draw_boxes_shipped_overtime_per_countries_linechart(sales_peoples_sales)

        # charts about products:
        # chart for comparing number of boxes shipped for different products 
        st.subheader("Boxes of products sold")
        draw_boxes_shipped_per_product_barchart(sales_peoples_sales)

        # chart for comparing sales amount obtained from different products
        st.subheader("Sales amount (USD) comparison between products")
        draw_sales_amount_per_product_barchart(sales_peoples_sales)

        # charts about sales people:
        # chart for comparing boxes sold by different sales people over time 
        st.subheader("Boxes of chocolates sold by sales people over time")
        draw_sales_person_boxes_shipped_linechart(sales_peoples_sales)

    except Exception as e: 
        print(e)
        st.error("Failed to get data from database" )

########################## CREATE THE DASHBOARD #################################
create_dashboard()