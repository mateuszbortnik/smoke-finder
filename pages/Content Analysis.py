import streamlit as st
import client
from client import RestClient
import pandas as pd
import time

st.title("Content Analysis")

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(keyword="logitech")

response = client.post("/v3/content_analysis/search/live", post_data)


if response["status_code"] == 20000:
    st.write("POST response:", response)
    task_id = response["tasks"][0]["id"]
    print("Task ID:", task_id)
else:
    print(f"POST error. Code: {response['status_code']} Message: {response['status_message']}")
    st.stop()

    # Wait a few seconds before checking task status
time.sleep(2)
