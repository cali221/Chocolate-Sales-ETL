import pandas as pd
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from scripts.utils import fetch_from_db

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
    # get dataframe from db's data
    online_store_product_quantity_ordered = fetch_from_db(sql_query, engine)

    # get the timestamp for last fetched time
    online_product_qty_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))

    # return last fetched time and dataframe
    return online_store_product_quantity_ordered, online_product_qty_last_fetched_at

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
    
    # get dataframe from db's data
    status_transition_durations = fetch_from_db(sql_query, engine)

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
    
    # get dataframe from db's data
    hourly_order_count = fetch_from_db(sql_query, engine)

    # convert the time to datetime to UTC
    hourly_order_count['hour'] = pd.to_datetime(hourly_order_count['hour'], utc=True)

    # convert the time to browser's timezone
    hourly_order_count['hour'] = hourly_order_count['hour'].dt.tz_convert(st.context.timezone)

    # create a column with hours range
    hourly_order_count['hours_range'] = (
        hourly_order_count['hour'].dt.strftime('%H:%M') + ' - ' +
        (hourly_order_count['hour'] + pd.Timedelta(hours=1)).dt.strftime('%H:%M')
    )

    print(hourly_order_count[['hours_range', 'hour', 'order_count']])

    # get timestamp for the last fetched time
    hourly_order_count_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))

    # return the dataframe and last fetched timestamp
    return hourly_order_count, hourly_order_count_last_fetched_at

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
    # get dataframe from db's data
    top_5_cust_countries = fetch_from_db(sql_query, engine)

    # get the timestamp for last fetched time
    top_5_cust_countries_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))

    # return last fetched time and dataframe
    return top_5_cust_countries, top_5_cust_countries_last_fetched_at

def load_online_store_hourly_revenue(engine):
    sql_query = """
                WITH hours AS(
                    SELECT generate_series(
                        DATE_TRUNC('hour', NOW() - INTERVAL '24 hours'),
                        DATE_TRUNC('hour', NOW()),
                        INTERVAL '1 hour'
                    ) AS hour
                ),
                revenue_per_order AS(
                    SELECT oi.order_item_order_id, 
                            oi.order_created_at,
                            SUM((oi.order_item_price_per_unit_at_purchase_usd - oi.discount_per_unit_amount_usd) * oi.order_item_quantity) AS subtotal,
                            SUM(oi.alloc_discount_off_order_amount_usd) AS discount_off_order,
                            SUM((oi.order_item_price_per_unit_at_purchase_usd - oi.discount_per_unit_amount_usd) * oi.order_item_quantity) - SUM(oi.alloc_discount_off_order_amount_usd) AS revenue
                    FROM marts.fct_online_store_ordered_items oi   
                    GROUP BY oi.order_item_order_id, order_created_at
                )

                SELECT h.hour AS hour, COALESCE(SUM(r.revenue), 0) AS revenue_per_hour
                FROM hours h
                LEFT JOIN revenue_per_order r
                ON r.order_created_at >= h.hour AND
                r.order_created_at < h.hour + interval '1 hour'
                GROUP BY h.hour
                ORDER BY h.hour ASC
                """

    # get dataframe from db's data
    hourly_rev = fetch_from_db(sql_query, engine)

    # convert the time to datetime to UTC
    hourly_rev['hour'] = pd.to_datetime(hourly_rev['hour'], utc=True)

    # convert the time to browser's timezone
    hourly_rev['hour'] = hourly_rev['hour'].dt.tz_convert(st.context.timezone)

    # create a column with hours range
    hourly_rev['hours_range'] = (
        hourly_rev['hour'].dt.strftime('%H:%M') + ' - ' +
        (hourly_rev['hour'] + pd.Timedelta(hours=1)).dt.strftime('%H:%M')
    )

    # get the timestamp for last fetched time
    hourly_rev_last_fetched_at = datetime.now(ZoneInfo(st.context.timezone))

    # return last fetched time and dataframe
    return hourly_rev, hourly_rev_last_fetched_at