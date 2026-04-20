import streamlit as st
from load_data import *
from online_store_sales_charts import *
from datetime import timedelta

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_online_prod_qty_chart(engine):
    """
    auto-refreshing chart for the bar chart
    showing the quantity ordered for different 
    products sold in online store
    """
    try:
        # load dataframe and last fetched time
        ordered_item_qty, online_product_qty_last_fetched_at = load_online_store_products_quantities_ordered_data(engine)

        # show caption for last fetched time
        st.caption(f"Last fetched at: {online_product_qty_last_fetched_at}")

        # draw chart using dataframe
        draw_item_quantities_ordered_online_barchart(ordered_item_qty) 
    except Exception as e:
        st.error(e)

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_online_status_transition_durations_chart(engine):
    """
    auto-refreshing chart for the bar chart showing
    the average time for orders' status transitions
    """
    try:
        # load dataframe and last fetched time
        order_status_transition_durations, order_status_transition_durations_last_fetched_at = load_online_status_transition_avg_time(engine)
        
        # show caption for last fetched time
        st.caption(f"Last fetched at: {order_status_transition_durations_last_fetched_at}")

        # draw chart using dataframe
        draw_online_status_transition_durations_barchart(order_status_transition_durations)
    except Exception as e:
        st.error(e)

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_online_hourly_order_count(engine):
    try:
        # load dataframe and last fetched time
        hourly_order_count, hourly_order_count_last_fetched_at = load_hourly_order_count_data(engine)

        # show caption for last fetched time
        st.caption(f"Last fetched at: {hourly_order_count_last_fetched_at}")

        # draw chart using dataframe
        draw_hourly_order_count_linechart(hourly_order_count)
    except Exception as e:
        st.error(e)

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_top_5_cust_countries(engine):
    try:
        # load dataframe and last fetched time
        top_5_cust_countries, top_5_cust_countries_last_fetched_at = load_top_5_cust_countries_online_store(engine)

        # show caption for last fetched time
        st.caption(f"Last fetched at: {top_5_cust_countries_last_fetched_at}")

        # draw chart using dataframe
        draw_top_5_cust_countries_barchart(top_5_cust_countries)
    except Exception as e:
        st.error(e)

@st.fragment(run_every=timedelta(minutes=15))
def refreshing_online_hourly_revenue(engine):
    try:
        # load dataframe and last fetched time
        hourly_rev, hourly_rev_last_fetched_at = load_online_store_hourly_revenue(engine)

        # show caption for last fetched time
        st.caption(f"Last fetched at: {hourly_rev_last_fetched_at}")

        # draw chart using dataframe
        draw_hourly_revenue_linechart(hourly_rev)
    except Exception as e:
        st.error(e)