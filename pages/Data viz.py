import pygwalker as pyg
import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
 
# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
 
# Add Title
st.title("Use Pygwalker In Streamlit")
 
uploaded_file = st.file_uploader("Choose a csv file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)


    # Generate the HTML using Pygwalker
    pyg_html = pyg.walk(df, return_html=True)
    
    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=1000, scrolling=True)
