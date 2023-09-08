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
    alias=alias)

    response = client.post("/v3/business_data/yelp/reviews/task_post", post_data)
    
    if response["status_code"] == 20000:
        print("POST response:", response)
        task_id = response["tasks"][0]["id"]
        print("Task ID:", task_id)
    else:
        print(f"POST error. Code: {response['status_code']} Message: {response['status_message']}")
        st.stop()