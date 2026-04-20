import streamlit as st
from scripts.data_loading_scripts.sales_peoples_sales_data_loading_script import load_sales_peoples_sales_data
from scripts.chart_drawing_scripts.sales_people_sales_charts import draw_pie_chart_for_boxes_shipped_per_country, \
                                                                    draw_boxes_shipped_overtime_per_countries_linechart, \
                                                                    draw_boxes_shipped_per_product_barchart, \
                                                                    draw_sales_amount_per_product_barchart, \
                                                                    draw_sales_person_boxes_shipped_linechart
                                          

def draw_sales_peoples_sales_dashboard_section(engine):
     # title for charts for sales people's sales
    st.title("Chocolate Sales by Sales People Between 2022 to 2024")
    st.markdown("**Charts for sales people's sales are static**")

    try:
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
        st.error(e)