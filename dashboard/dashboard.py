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
    # get the dataframe
    sales_peoples_sales = pd.read_sql(sql_query, engine)
    return sales_peoples_sales

def load_online_store_products_quantities_ordered_data(engine):
    """
    load data for quantity ordered for online store's products 
    and last fetched time
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
    # get the dataframe 
    online_store_product_quantity_ordered = pd.read_sql(sql_query, engine)

    # get the timestamp for last fetched time
    online_product_qty_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))

    # return last fetched time and dataframe
    return online_store_product_quantity_ordered, online_product_qty_last_fetched_at

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_online_prod_qty_chart(engine):
    """
    auto-refreshing chart for the bar chart
    showing the quantity ordered for different 
    products sold in online store
    """
    # load dataframe and last fetched time
    ordered_item_qty, online_product_qty_last_fetched_at = load_online_store_products_quantities_ordered_data(engine)

    # show caption for last fetched time
    st.caption(f"Last fetched at: {online_product_qty_last_fetched_at}")

    # draw chart using dataframe
    draw_item_quantities_ordered_online_barchart(ordered_item_qty)

def load_online_status_transition_avg_time(engine):
    """
    load the average time data for orders' status transitions
    and the last fetched time
    """
    sql_query = """
                SELECT AVG(EXTRACT(EPOCH FROM (order_started_processing_at - order_started_pending_at)) / 3600) AS pending_to_processing_hrs,
                       AVG(EXTRACT(EPOCH FROM (order_started_in_transit_at - order_started_processing_at)) / 3600) AS processing_to_in_transit_hrs,
                       AVG(EXTRACT(EPOCH FROM (order_arrived_at - order_started_in_transit_at)) / 3600) AS in_transit_to_arrived_hrs,
                       AVG(EXTRACT(EPOCH FROM (order_completed_at - order_arrived_at)) / 3600) AS arrived_to_completed_hours
                FROM marts.fct_online_store_ordered_items
                """
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

    # get the timestamp for last fetched time
    online_status_transition_durations_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))

    # return the dataframe and the last fetched timestamp
    return res_df, online_status_transition_durations_last_fetched_at 

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_online_status_transition_durations_chart(engine):
    """
    auto-refreshing chart for the bar chart showing
    the average time for orders' status transitions
    """
    # load dataframe and last fetched time
    order_status_transition_durations, order_status_transition_durations_last_fetched_at = load_online_status_transition_avg_time(engine)
    
    # show caption for last fetched time
    st.caption(f"Last fetched at: {order_status_transition_durations_last_fetched_at}")

    # draw chart using dataframe
    draw_online_status_transition_durations_barchart(order_status_transition_durations)

def load_hourly_order_count_data(engine):
    """
    load the data for hourly order count
    for orders from the online store
    """
    sql_query = f"""
                WITH hours AS(
                    SELECT generate_series(
                        DATE_TRUNC('hour', NOW() - INTERVAL '24 hours'),
                        DATE_TRUNC('hour', NOW()),
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
    
    # fetch data from db
    hourly_order_count = pd.read_sql(sql_query, engine)

    # convert the time to datetime to UTC
    hourly_order_count['hour'] = pd.to_datetime(hourly_order_count['hour'], utc=True)

    # convert the time to browser's timezone
    hourly_order_count['hour'] = hourly_order_count['hour'].dt.tz_convert(st.context.timezone)

    # create a column with hours range
    hourly_order_count['hours_range'] = (
        hourly_order_count['hour'].dt.strftime('%H:%M') + ' - ' +
        (hourly_order_count['hour'] + pd.Timedelta(hours=1)).dt.strftime('%H:%M')
    )

    # get timestamp for the last fetched time
    hourly_order_count_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))

    # return the dataframe and last fetched timestamp
    return hourly_order_count, hourly_order_count_last_fetched_at

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_online_hourly_order_count(engine):
    # load dataframe and last fetched time
    hourly_order_count, hourly_order_count_last_fetched_at = load_hourly_order_count_data(engine)

    # show caption for last fetched time
    st.caption(f"Last fetched at: {hourly_order_count_last_fetched_at}")

    # draw chart using dataframe
    draw_hourly_order_count_linechart(hourly_order_count)
    
def load_top_5_cust_countries_online_store(engine):
    """
    load the data for top 5 online store customers' countries
    """
    sql_query = """
                SELECT COUNT(DISTINCT(oi.order_item_order_id)) AS order_count,
                       co.country_name, 
                       oi.order_customer_country_id
                FROM marts.fct_online_store_ordered_items oi
                JOIN marts.dim_customers_countries co
                ON co.country_id = oi.order_customer_country_id
                GROUP BY oi.order_customer_country_id, co.country_name
                ORDER BY COUNT(oi.order_item_order_id) DESC
                LIMIT 5
                """
    top_5_cust_countries = pd.read_sql(sql_query, engine)

    # get the timestamp for last fetched time
    top_5_cust_countries_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))

    # return last fetched time and dataframe
    return top_5_cust_countries, top_5_cust_countries_last_fetched_at

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_top_5_cust_countries(engine):
    # load dataframe and last fetched time
    top_5_cust_countries, top_5_cust_countries_last_fetched_at = load_top_5_cust_countries_online_store(engine)

    # show caption for last fetched time
    st.caption(f"Last fetched at: {top_5_cust_countries_last_fetched_at}")

    # draw chart using dataframe
    draw_top_5_cust_countries_barchart(top_5_cust_countries)

def create_dashboard(): 
    """
    create the dashboard showing charts about the data
    """   
    try:
        engine = get_engine()

        # testing area -> delete later
        #load_hourly_order_count_data(engine)

        # ------------------------ online store sales ----------------------------
        # title for charts for online store sales
        st.title("Online Store Sales")
        st.caption("Charts for online store sales are updated every 15 minutes")

        st.subheader("Comparison of quantities ordered between products (all tinme)")
        refreshing_online_prod_qty_chart(engine)

        st.subheader("Average orders' status transition durations (all time)")
        refreshing_online_status_transition_durations_chart(engine)

        st.subheader("Hourly order count in the last 24 hours")
        refreshing_online_hourly_order_count(engine)

        st.subheader("Top 5 customers' countries making the largest number of orders (all time)")
        refreshing_top_5_cust_countries(engine)

        # ------------------- sales people's sales --------------------
        # title for charts for sales people's sales
        st.title("Chocolate Sales by Sales People Between 2022 to 2024")
        st.caption("Charts for sales people's sales are static")

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