import streamlit as st
import pandas as pd
import altair as alt

def draw_item_quantities_ordered_online_barchart(df):       
    """
    draw the bar chart showing comparison of the quantity
    ordered for different products sold in online store
    """                                         
    products_quantity_ordered_barchart = alt.Chart(df).mark_bar().encode(
        alt.Y("product_name:N", axis=alt.Axis(labelLimit=1000)).title("Product name"),
        alt.X("sum(ordered_quantity):Q", axis=alt.Axis(tickMinStep=1)).title("Total quantity ordered")
    )
    
    st.altair_chart(products_quantity_ordered_barchart)

def draw_online_status_transition_durations_barchart(df):
    """
    draw the bar chart showing the average duration of online orders'
    status transitions 
    """
    status_transition_durations = alt.Chart(df).mark_bar().encode(
        alt.Y("transitions:N", axis=alt.Axis(labelLimit=1000)).title("Status transition"),
        alt.X("durations:Q").title("Average duration of transition (hours)")
    )
    
    st.altair_chart(status_transition_durations)

def draw_hourly_order_count_linechart(df):
    """
    draw the line chart showing the hourly number of 
    orders form online store in the last 24 hours
    """
    hourly_order_count_linechart = alt.Chart(df).mark_line().encode(
        alt.X("hours_range:N", sort=alt.EncodingSortField('hour')).title("Hours range"),
        alt.Y("order_count:Q", axis=alt.Axis(tickMinStep=1)).title("Number of orders")
    )

    # draw the line chart
    st.altair_chart(hourly_order_count_linechart)

def draw_top_5_cust_countries_barchart(df):
    """
    draw bar chart showing online store customers'
    countries that make the higher number of orders
    """
    top_5_cust_countries = alt.Chart(df).mark_bar().encode(
        alt.X("order_count:Q", axis=alt.Axis(tickMinStep=1)).title("Number of orders"),
        alt.Y("country_name:N").sort('-x').title("Country")
    )
    
    st.altair_chart(top_5_cust_countries)

def draw_hourly_revenue_linechart(df):
    """
    draw the line chart showing the hourly 
    revenue from online store in the last 24 hours
    """
    hourly_revenue_linechart = alt.Chart(df).mark_line().encode(
        alt.X("hours_range:N", sort=alt.SortField('hour')).title("Hours range"),
        alt.Y("revenue_per_hour:Q").title("Revenue ($)")
    )

    # draw the line chart
    st.altair_chart(hourly_revenue_linechart)