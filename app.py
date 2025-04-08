import streamlit as st

st.set_page_config(
    page_title="Data Explorer App",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Data Explorer App")
st.markdown("""

* Search for movie information from a database
* Analyze your own CSV data files

Select a page from the sidebar to get started.
""")

# Add some example images or further instructions
st.subheader("How to use this app")
st.markdown("""
1. Use the **Movie Database** page to search for information about movies
2. Use the **CSV Analyzer** page to upload and analyze your own CSV data files
3. search the **covid stats** for a chosen country
""")

# Show a sample of what can be done
st.subheader("Application Features")
col1, col2,col3  = st.columns(3)
    
with col1:
    st.markdown("### Movie Database")
    st.markdown("Search movie information from OMDB API")
    
with col2:
    st.markdown("### CSV Analyzer")
    st.markdown("Upload and analyze your own data files")
with col3:
    st.markdown("### Covid Stats")
    st.markdown("Search a country")



    
