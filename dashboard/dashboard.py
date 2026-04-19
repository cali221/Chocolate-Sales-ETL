import streamlit as st
import pandas as pd
import altair as alt
from utils import get_engine
from sales_people_sales_charts import *
from online_store_sales_charts import *
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def load_sales_peoples_sales_data(engine):
    """
    load the sales data attributed to sales people from the database
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
    sales_peoples_sales = pd.read_sql(sql_query, engine)
    return sales_peoples_sales

def load_online_store_products_quantities_ordered_data(_engine):
    """
    quantity ordered for online store's products 
    """
    sql_query= """
              SELECT COALESCE(oi.order_item_quantity, 0) AS ordered_quantity, 
                     p.product_id, 
                     p.product_name,
                     oi.order_created_at,
                     oi.order_item_order_id
               FROM marts.fct_online_store_ordered_items oi
               RIGHT JOIN marts.dim_products p 
               ON p.product_id = oi.order_item_product_id 
               """
    online_store_product_quantity_ordered = pd.read_sql(sql_query, _engine)
    online_product_qty_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))
    return online_store_product_quantity_ordered, online_product_qty_last_fetched_at

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_online_prod_qty_chart(engine):
    ordered_item_qty, online_product_qty_last_fetched_at = load_online_store_products_quantities_ordered_data(engine)
    st.caption(f"Last fetched at: {online_product_qty_last_fetched_at}")
    draw_item_quantities_ordered_online_barchart(ordered_item_qty)

def load_online_status_transition_avg_time(engine):
    sql_query = """
                SELECT AVG(EXTRACT(EPOCH FROM (order_started_processing_at - order_started_pending_at)) / 3600) AS pending_to_processing_hrs,
                       AVG(EXTRACT(EPOCH FROM (order_started_in_transit_at - order_started_processing_at)) / 3600) AS processing_to_in_transit_hrs,
                       AVG(EXTRACT(EPOCH FROM (order_arrived_at - order_started_in_transit_at)) / 3600) AS in_transit_to_arrived_hrs,
                       AVG(EXTRACT(EPOCH FROM (order_completed_at - order_arrived_at)) / 3600) AS arrived_to_completed_hours
                FROM marts.fct_online_store_ordered_items
                """
    # get the dataframe with one row and 4 columns (one for each transition)
    status_transition_durations = pd.read_sql(sql_query, engine)

    # convert the dataframe so it has one row for each transition
    # get the values as an array
    vals_arr = [status_transition_durations['pending_to_processing_hrs'].iloc[0],
                status_transition_durations['processing_to_in_transit_hrs'].iloc[0],
                status_transition_durations['in_transit_to_arrived_hrs'].iloc[0],
                status_transition_durations['arrived_to_completed_hours'].iloc[0]]
    
    # create the resulting dataframe
    res_df = pd.DataFrame(
        {
            "transitions": ["Pending ▶ Processing", 
                            "Processing ▶ In Transit",
                            "In Transit ▶ Arrived",
                            "Arrived ▶ Completed"],
            "durations": vals_arr
        }
    )

    online_status_transition_durations_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))
    return res_df, online_status_transition_durations_last_fetched_at 

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_online_status_transition_durations_chart(engine):
    order_status_transition_durations, order_status_transition_durations_last_fetched_at = load_online_status_transition_avg_time(engine)
    st.caption(f"Last fetched at: {order_status_transition_durations_last_fetched_at}")
    draw_online_status_transition_durations_barchart(order_status_transition_durations)

def load_hourly_order_count_data(engine):
    sql_query = f"""
                WITH hours AS(
                SELECT generate_series(
                    NOW() - INTERVAL '24 hours',
                    NOW(),
                    INTERVAL '1 hour'
                ) AS hour
                )

                SELECT h.hour AS hour, COUNT(DISTINCT oi.order_item_order_id) AS order_count
                FROM hours h
                LEFT JOIN marts.fct_online_store_ordered_items oi
                ON oi.order_created_at >= h.hour AND
                oi.order_created_at < h.hour + interval '1 hour'
                GROUP BY h.hour
                ORDER BY h.hour ASC
                """
    
    hourly_order_count = pd.read_sql(sql_query, engine)

    hourly_order_count['hour'] = pd.to_datetime(hourly_order_count['hour'], utc=True)
    hourly_order_count['hour'] = hourly_order_count['hour'].dt.tz_convert(st.context.timezone)

    hourly_order_count_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))
    return hourly_order_count, hourly_order_count_last_fetched_at
    
def create_dashboard(): 
    """
    create the dashboard showing charts about the data
    """   
    try:
        engine = get_engine()

        # testing area -> delete later
        load_hourly_order_count_data(engine)

        # ------------------------ online store sales ----------------------------
        # title for charts for online store sales
        st.title("Online Store Sales")
        st.caption("Charts for online store sales are updated every 15 minutes")

        st.subheader("Comparison of quantities ordered between products")
        refreshing_online_prod_qty_chart(engine)

        st.subheader("Average orders' status transition durations")
        refreshing_online_status_transition_durations_chart(engine)

        # ------------------- sales people's sales --------------------
        # title for charts for sales people's sales
        st.title("Chocolate Sales by Sales People Between 2022 to 2024")

        # get data for the sales people's sales data (shared between charts)
        sales_peoples_sales = load_sales_peoples_sales_data(engine)

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

# create the dashboard
create_dashboard()