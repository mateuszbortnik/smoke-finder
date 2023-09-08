import streamlit as st
import client
from client import RestClient
import pandas as pd
import time


st.title("Yelp reviews")

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

alias = st.text_input('Alias', 'ashley-stewart-hawthorne')

if st.button('Get data'):
    # POST request to enqueue a task
    post_data = dict()

    post_data[len(post_data)] = dict(
    language_name="English",
    alias=alias
)