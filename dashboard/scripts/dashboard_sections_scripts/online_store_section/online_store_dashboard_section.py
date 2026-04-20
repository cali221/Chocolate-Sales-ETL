import streamlit as st
from scripts.dashboard_sections_scripts.online_store_section.refreshing_online_store_charts_section import refreshing_online_hourly_order_count, \
                                                                                                           refreshing_online_hourly_revenue, \
                                                                                                           refreshing_online_prod_qty_chart, \
                                                                                                           refreshing_online_status_transition_durations_chart, \
                                                                                                           refreshing_top_5_cust_countries

def draw_online_store_dashboard_section(engine):
    st.title("Online Store Sales")
    st.markdown("**Charts for online store sales are updated every 15 minutes**")

    st.subheader("Hourly order count in the last 24 hours")
    # line chart showing hourly order count in the last 24 hours
    refreshing_online_hourly_order_count(engine)

    st.subheader("Hourly revenue in the last 24 hours")
    # line chart showing hourly revenue in the last 24 hours
    refreshing_online_hourly_revenue(engine)

    st.subheader("Comparison of quantities ordered between products (all time)")
    # bar chart showing average duration of online order status transitions
    refreshing_online_prod_qty_chart(engine)

    st.subheader("Average orders' status transition durations (all time)")
    # bar chart showing average duration of online order status transitions
    refreshing_online_status_transition_durations_chart(engine)

    st.subheader("Top 5 customers' countries making the largest number of orders (all time)")
    # bar chart showing top 5 customers' countries that made the most orders
    refreshing_top_5_cust_countries(engine)