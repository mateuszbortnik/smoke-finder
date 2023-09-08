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
        st.write("POST response:", response)
        task_id = response["tasks"][0]["id"]
        print("Task ID:", task_id)
    else:
        print(f"POST error. Code: {response['status_code']} Message: {response['status_message']}")
        st.stop()


    # Wait a few seconds before checking task status
    time.sleep(2)

    # GET request to fetch the results of the task
    MAX_RETRIES = 10
    WAIT_TIME = 10
    retry_count = 0
    task_ready = False

    while retry_count < MAX_RETRIES and not task_ready:
        # st.write(f"Retry count: {retry_count}")  # Debugging line
        response = client.get(f"/v3/business_data/yelp/reviews/task_get/{task_id}")
        st.write("GET response:", response)

        if response['status_code'] == 20000:
            task_status = response['tasks'][0]['status_message']
            st.write(f"Task status: {task_status}")  # Debugging line
            if task_status == "Task In Queue":
                # st.write(f"Attempt {retry_count + 1}: Task is still in queue. Retrying in {WAIT_TIME} seconds...")
                retry_count += 1
                time.sleep(WAIT_TIME)
            elif task_status == "Ok.":  # Only set task_ready = True when the task is actually complete
                task_ready = True
                # st.write("Task is ready.")  # Debugging line
        else:
            st.write(f"GET error. Code: {response['status_code']} Message: {response['status_message']}")
            break
