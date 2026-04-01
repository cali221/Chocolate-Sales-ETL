import streamlit as st
import pandas as pd
import altair as alt
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

def load_sales_data():
    """
    load the sales data from the database
    """
    load_dotenv()
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

    # get all required data by joining tables
    sql_query = """
                SELECT s.sales_amount_usd,
                       s.boxes_shipped,
                       s.date,
                       c.name AS country,
                       sp.name AS sales_person,
                       p.name AS product
                FROM sales s
                JOIN country c ON c.id = s.country_id
                JOIN sales_person sp ON sp.id = s.sales_person_id
                JOIN product p on p.id = s.product_id
                """
    sales_df = pd.read_sql(sql_query, engine)
    return sales_df

def create_dashboard(): 
    """
    create the dashboard showing charts about the data
    """   
    try:
        # get data
        sales_df = load_sales_data()

        # dashboard's title
        st.title("Chocolate Sales Between 2022 to 2024")

        ############################### CHARTS ABOUT BOXES SHIPPED OVERALL ###################################
        # --------- chart for comparing total boxes shipped between countries --------------
        st.subheader("Comparison of total chocolate boxes shipped between countries")

        # date range selector
        date_range_selected_boxes_shipped_countries = st.date_input("Select Date Range", 
                                                      [sales_df["date"].min(), sales_df["date"].max()], 
                                                      key="countries-boxes-shipped-dates")

        # if start and end date for date range is selected draw chart
        if len(date_range_selected_boxes_shipped_countries) == 2: 
            # filtered df based on selected date range
            filtered_df_countries_boxes_shipped = sales_df[sales_df["date"].between(date_range_selected_boxes_shipped_countries[0], 
                                                                                    date_range_selected_boxes_shipped_countries[1])]
            
            # create piechart based on the filtered df
            boxes_shipped_countries_piechart = alt.Chart(filtered_df_countries_boxes_shipped).mark_arc().encode(
                theta="sum(boxes_shipped)",
                color="country"
            )

            # draw the pie chart
            st.altair_chart(boxes_shipped_countries_piechart)
        else:
            st.info("Please pick one start date and one end date")

        # --------- chart for showing the number of boxes shipped over time --------------
        st.subheader("Chocolate boxes shipped over time")

        # countries selector
        selected_countries = st.multiselect("Select Countries", 
                                            sales_df["country"].unique(), 
                                            default=["UK"], 
                                            key="boxes-chart-countries")
        
        # filter df based on selected country (default selected country is UK)
        filtered_df_boxes_shipped_overtime_per_country = sales_df[sales_df["country"].isin(selected_countries)]

        # date selector
        date_range_selected_boxes_shipped_per_country_over_time = st.date_input("Select Date Range", 
                                                                [sales_df["date"].min(), 
                                                                sales_df["date"].max()], 
                                                                key="boxes-chart-dates")
        
        # if start and end date for date range is selected, draw the chart
        if len(date_range_selected_boxes_shipped_per_country_over_time) == 2:
            # filter the filtered df (previously filtered based on selected country) based on selected date range
            filtered_df_boxes_shipped_overtime_per_country = filtered_df_boxes_shipped_overtime_per_country[filtered_df_boxes_shipped_overtime_per_country["date"].
                                                                                                            between(date_range_selected_boxes_shipped_per_country_over_time[0], 
                                                                                                                    date_range_selected_boxes_shipped_per_country_over_time[1])]

            # create line chart
            boxes_shipped_overtime_linechart = alt.Chart(filtered_df_boxes_shipped_overtime_per_country).mark_line().encode(
                alt.X("date:T", axis=alt.Axis(format="%Y/%m/%d")),
                alt.Y("sum(boxes_shipped):Q").title("Total boxes shipped"),
                color="country:N",
            )

            # draw the line chart
            st.altair_chart(boxes_shipped_overtime_linechart)
        else:
            st.info("Please pick one start date and one end date")

        ################################ CHARTS ABOUT PRODUCTS ##################################################
        # ------------------- chart for comparing number of boxes shipped for different products ---------------- 
        st.subheader("Boxes of products sold")

        # countries selector
        selected_countries_boxes_shipped_by_products = st.multiselect("Select Countries", 
                                                                    sales_df["country"].unique(), 
                                                                    default=["UK"], 
                                                                    key="product-chart-countries")
        
        # sales_df filtered according countries selected (default is UK)
        filtered_df_boxes_shipped_by_products = sales_df[sales_df["country"].isin(selected_countries_boxes_shipped_by_products)]

        # date range selector
        date_range_selected_boxes_shipped_by_products = st.date_input("Select Date Range", 
                                                                    [sales_df["date"].min(), sales_df["date"].max()], 
                                                                    key="product-chart-dates")
        
        # if start and end date for date range are selected, draw chart
        if len(date_range_selected_boxes_shipped_by_products) == 2: 
            # filtered dataframe (previously filtered according to selected countries) filtered according to date range selected
            filtered_df_boxes_shipped_by_products = filtered_df_boxes_shipped_by_products[filtered_df_boxes_shipped_by_products["date"].
                                                                                        between(date_range_selected_boxes_shipped_by_products[0], 
                                                                                                date_range_selected_boxes_shipped_by_products[1])]

            # create the bar chart
            products_sold_barchart = alt.Chart(filtered_df_boxes_shipped_by_products).mark_bar().encode(
                alt.X("product:N"),
                alt.Y("sum(boxes_shipped):Q").title("Total boxes shipped")
            )

            # draw the bar chart
            st.altair_chart(products_sold_barchart)
        else:
            st.info("Please pick one start date and one end date")

        # ------------- chart for comparing sales amount obtained from different products ------------------------
        st.subheader("Sales amount (USD) comparison between products")

        # countries selector
        selected_countries_product_amount = st.multiselect("Select Countries", 
                                                            sales_df["country"].unique(), 
                                                            default=["UK"], 
                                                            key="product-amount-chart-countries")
        
        # filter sales_df according to the selected countries (default is UK)
        filtered_df_products_amount = sales_df[sales_df["country"].isin(selected_countries_product_amount)]

        # date range selector
        date_range_selected_products_amount = st.date_input("Select Date Range", 
                                                            [sales_df["date"].min(), sales_df["date"].max()], 
                                                            key="product-amount-chart-dates")
        
        # if start and end date for date range are selected, draw chart
        if len(date_range_selected_products_amount) == 2:
            # filter the filtered df (previously filtered according to selected countries) according to selected date range
            filtered_df_products_amount = filtered_df_products_amount[filtered_df_products_amount["date"].
                                                                    between(date_range_selected_products_amount[0], 
                                                                            date_range_selected_products_amount[1])]

            # create the bar chart
            products_sold_barchart = alt.Chart(filtered_df_products_amount).mark_bar().encode(
                alt.X("product:N"),
                alt.Y("sum(sales_amount_usd):Q").title("Total amount (USD)")
            )

            # draw the bar chart
            st.altair_chart(products_sold_barchart)
        else:
            st.info("Please pick one start date and one end date")

        ################################ CHARTS ABOUT SALES PERSON ##################################################
        # ---------------- chart for comparing boxes sold by different sales people over time -------------------------
        st.subheader("Boxes of chocolates sold by sales people over time")

        # sales people selector
        selected_sales_people = st.multiselect("Select Sales People", 
                                            sales_df["sales_person"].unique(), 
                                            default=["Jehu Rudeforth"], 
                                            key="sales-person-chart-people")
        
        # sales_df filtered according to sales people selected (default is Jehu Rudeforth)
        filtered_df_sales_person_boxes_shipped = sales_df[sales_df["sales_person"].isin(selected_sales_people)]
        
        # date range selector 
        date_range_selected_sales_person_boxes_shipped = st.date_input("Select Date Range", 
                                                        [sales_df["date"].min(), 
                                                        sales_df["date"].max()], 
                                                        key="sales-person-boxes-shipped-chart")
        
        # if start and end dates for the date range are selected, draw the chart
        if len(date_range_selected_sales_person_boxes_shipped) == 2:
            # filter the filtered df (previously filtered according to selected sales people) according to the selected date range
            filtered_df_sales_person_boxes_shipped = filtered_df_sales_person_boxes_shipped[filtered_df_sales_person_boxes_shipped["date"].
                                                                                            between(date_range_selected_sales_person_boxes_shipped[0], 
                                                                                                    date_range_selected_sales_person_boxes_shipped[1])]

            # create the line chart
            boxes_shipped_overtime_linechart = alt.Chart(filtered_df_sales_person_boxes_shipped).mark_line().encode(
                alt.X("date:T", axis=alt.Axis(format="%Y/%m/%d")),
                alt.Y("sum(boxes_shipped):Q").title("Total boxes shipped"),
                color="sales_person:N",
            )

            # draw the line chart
            st.altair_chart(boxes_shipped_overtime_linechart)
        else:
            st.info("Please pick one start date and one end date")
    except:
        st.error("Failed to get data from database")

        

########################## CREATE THE DASHBOARD #################################
create_dashboard()