import streamlit as st
from utils import get_engine
from sales_people_sales_charts import *
from load_data import *
from refreshing_charts import *

def create_dashboard(): 
    """
    create the dashboard showing charts about the data
    """   
    try:
        engine = get_engine()

        # -------------------------- online store sales ------------------------------
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

        # -------------------------- sales people's sales ----------------------------
        # title for charts for sales people's sales
        st.title("Chocolate Sales by Sales People Between 2022 to 2024")
        st.markdown("**Charts for sales people's sales are static**")

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