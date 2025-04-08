import streamlit as st
from src.ui.layout import make_sidebar

st.set_page_config(page_title="World Insights App", layout="wide")
make_sidebar()

st.title("orld Insights Dashboard")
st.write("Welcome! Use the sidebar to navigate between Weather, Country Info, and COVID-19 statistics.")
