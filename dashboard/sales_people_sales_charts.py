import streamlit as st
import pandas as pd
import altair as alt
from utils import validate_time_range_and_filter

def draw_pie_chart_for_boxes_shipped_per_country(df):
    """
    draw the pie chart showing boxes shipped per country
    (for sales people's sales data)
    """
    # date range selector
    date_range_selected_boxes_shipped_countries = st.date_input("Select Date Range", 
                                                  [df["date"].min(), df["date"].max()], 
                                                  key="countries-boxes-shipped-dates")

    filtered_df_countries_boxes_shipped, error_msg = validate_time_range_and_filter(date_range_selected_boxes_shipped_countries, 
                                                                                    df,
                                                                                    "date")

    # if date range is invalid show error message
    if error_msg:
        st.info(error_msg)
    else:
        # create the chart
        boxes_shipped_countries_piechart = alt.Chart(filtered_df_countries_boxes_shipped).mark_arc().encode(
            theta="sum(boxes_shipped):Q",
            color="country:N"
        )
        # draw the pie chart
        st.altair_chart(boxes_shipped_countries_piechart)


def draw_boxes_shipped_overtime_per_countries_linechart(df):
    """
    draw the linechart showing the number of boxes shipped
    overtime for different countries
    (for sales people's sales data)
    """
    # countries selector
    selected_countries = st.multiselect("Select Countries", 
                                        df["country"].unique(), 
                                        default=["United Kingdom"], 
                                        key="boxes-chart-countries")
    
    # filter df based on selected country (default selected country is UK)
    filtered_df_boxes_shipped_overtime_per_country = df[df["country"].isin(selected_countries)]

    # date selector
    date_range_selected_boxes_shipped_per_country_over_time = st.date_input("Select Date Range", 
                                                                            [df["date"].min(), 
                                                                             df["date"].max()], 
                                                                            key="boxes-chart-dates")
    
    filtered_df_boxes_shipped_overtime_per_country, error_msg = validate_time_range_and_filter(date_range_selected_boxes_shipped_per_country_over_time, 
                                                                                               filtered_df_boxes_shipped_overtime_per_country,
                                                                                               "date")
    # if date range is invalid show error message
    if error_msg:
        st.info(error_msg)
    else:
        boxes_shipped_overtime_linechart = alt.Chart(filtered_df_boxes_shipped_overtime_per_country).mark_line().encode(
            alt.X("date:T", axis=alt.Axis(format="%Y/%m/%d")),
            alt.Y("sum(boxes_shipped):Q").title("Total boxes shipped"),
            color="country:N",
        )
        # draw the line chart
        st.altair_chart(boxes_shipped_overtime_linechart)

def draw_boxes_shipped_per_product_barchart(df):
    """
    draw the bar chart showing the number of boxes shipped
    for different products
    (for sales people's sales data)
    """
    # countries selector
    selected_countries_boxes_shipped_by_products = st.multiselect("Select Countries", 
                                                                  df["country"].unique(), 
                                                                  default=["United Kingdom"], 
                                                                  key="product-chart-countries")
    
    # sales_peoples_sales filtered according countries selected (default is UK)
    filtered_df_boxes_shipped_by_products = df[df["country"].isin(selected_countries_boxes_shipped_by_products)]

    # date range selector
    date_range_selected_boxes_shipped_by_products = st.date_input("Select Date Range", 
                                                                  [df["date"].min(), df["date"].max()], 
                                                                  key="product-chart-dates")
    filtered_df_boxes_shipped_by_products, error_msg = validate_time_range_and_filter(date_range_selected_boxes_shipped_by_products, 
                                                                                      filtered_df_boxes_shipped_by_products,
                                                                                      "date")
    # if date range is invalid show error message
    if error_msg:
        st.info(error_msg)
    else:
        # create the bar chart
        products_sold_barchart = alt.Chart(filtered_df_boxes_shipped_by_products).mark_bar().encode(
            alt.X("product:N"),
            alt.Y("sum(boxes_shipped):Q").title("Total boxes shipped")
        )

        # draw the bar chart
        st.altair_chart(products_sold_barchart)

def draw_sales_amount_per_product_barchart(df):
    """ 
    draw bar chart showing the sales amount for different products 
    (for sales people's sales data)
    """
    # countries selector
    selected_countries_product_amount = st.multiselect("Select Countries", 
                                                        df["country"].unique(), 
                                                        default=["United Kingdom"], 
                                                        key="product-amount-chart-countries")
    
    # filter sales_peoples_sales according to the selected countries (default is UK)
    filtered_df_products_amount = df[df["country"].isin(selected_countries_product_amount)]

    # date range selector
    date_range_selected_products_amount = st.date_input("Select Date Range", 
                                                        [df["date"].min(), df["date"].max()], 
                                                        key="product-amount-chart-dates")
    
    filtered_df_products_amount, error_msg = validate_time_range_and_filter(date_range_selected_products_amount, 
                                                                            filtered_df_products_amount,
                                                                            "date")
    # if date range is invalid show error message
    if error_msg:
        st.info(error_msg)
    else:
        # create the bar chart
        products_sold_barchart = alt.Chart(filtered_df_products_amount).mark_bar().encode(
            alt.X("product:N"),
            alt.Y("sum(sales_amount_usd):Q").title("Total amount ($)")
        )
        # draw the bar chart
        st.altair_chart(products_sold_barchart)

def draw_sales_person_boxes_shipped_linechart(df):
    """
    draw line chart shohwing boxes shipped
    attributed to different sales people
    (for sales people's sales data)
    """
    # sales people selector
    selected_sales_people = st.multiselect("Select Sales People", 
                                           df["sales_person"].unique(), 
                                           default=["Jehu Rudeforth"], 
                                           key="sales-person-chart-people")
    
    # sales_peoples_sales filtered according to sales people selected (default is Jehu Rudeforth)
    filtered_df_sales_person_boxes_shipped = df[df["sales_person"].isin(selected_sales_people)]
    
    # date range selector 
    date_range_selected_sales_person_boxes_shipped = st.date_input("Select Date Range", 
                                                     [df["date"].min(), 
                                                      df["date"].max()], 
                                                     key="sales-person-boxes-shipped-chart")
    
    filtered_df_sales_person_boxes_shipped, error_msg = validate_time_range_and_filter(date_range_selected_sales_person_boxes_shipped,
                                                                                       filtered_df_sales_person_boxes_shipped,
                                                                                       "date")
    # if date range is invalid show error message
    if error_msg:
        st.info(error_msg)
    else:
        # create the line chart
        boxes_shipped_overtime_linechart = alt.Chart(filtered_df_sales_person_boxes_shipped).mark_line().encode(
            alt.X("date:T", axis=alt.Axis(format="%Y/%m/%d")),
            alt.Y("sum(boxes_shipped):Q").title("Total boxes shipped"),
            color="sales_person:N",
        )

        # draw the line chart
        st.altair_chart(boxes_shipped_overtime_linechart)