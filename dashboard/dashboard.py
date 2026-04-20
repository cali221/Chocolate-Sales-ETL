import streamlit as st
from scripts.utils import get_engine
from scripts.dashboard_sections_scripts.online_store_section.online_store_dashboard_section import draw_online_store_dashboard_section
from scripts.dashboard_sections_scripts.sales_peoples_sales_section.sales_peoples_sales_dashboard_section import draw_sales_peoples_sales_dashboard_section

def create_dashboard(): 
    """
    create the dashboard showing charts about the data
    """   
    try:
        engine = get_engine()
    except Exception as e:
        st.error(e)
        st.stop()

    # online store sales
    draw_online_store_dashboard_section(engine)

    # sales people's sales
    draw_sales_peoples_sales_dashboard_section(engine)

# create the dashboard
create_dashboard()