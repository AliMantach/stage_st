import streamlit as st
from src.logic.covid_logic import get_covid_stats

st.title("🦠 COVID-19 Stats")

country = st.text_input("Enter a country name", "Germany")

if country:
    stats = get_covid_stats(country)
    if stats:
        st.metric("Total Cases", f"{stats['cases']:,}")
        st.metric("Total Deaths", f"{stats['deaths']:,}")
        st.metric("Recovered", f"{stats['recovered']:,}")
    else:
        st.error("Could not fetch COVID data.")
