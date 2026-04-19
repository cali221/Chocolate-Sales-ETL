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
    draw the bar chart showing the average duration of orders'
    status transitions
    """
    status_transition_durations = alt.Chart(df).mark_bar().encode(
        alt.Y("transitions:N", axis=alt.Axis(labelLimit=1000)).title("Status Transition"),
        alt.X("durations:Q").title("Average Duration of Transition (hours)")
    )
    
    st.altair_chart(status_transition_durations)
