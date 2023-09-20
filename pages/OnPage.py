import streamlit as st
import client
from client import RestClient
import pandas as pd
import time
from random import Random

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

st.title("OnPage")
st.text("")

target = st.text_input('Target', 'ashleystewart.com')

rnd = Random()
post_data = dict()

post_data[rnd.randint(1, 30000000)] = dict(
    target=target,
    max_crawl_pages=10
)

# POST /v3/on_page/task_post
# the full list of possible parameters is available in documentation
response = client.post("/v3/on_page/task_post", post_data)

if response["status_code"] == 20000:
    # st.write("POST response:", response)
    task_id = response["tasks"][0]["id"]
    # st.write("Task ID:", task_id)
else:
    st.write(f"POST error. Code: {response['status_code']} Message: {response['status_message']}")
    st.stop()


# GET request to fetch the results of the task
MAX_RETRIES = 10
WAIT_TIME = 10
retry_count = 0
task_ready = False

while retry_count < MAX_RETRIES and not task_ready:
    # st.write(f"Retry count: {retry_count}")  # Debugging line
    response = client.get(f"/v3/on_page/summary/{task_id}")
    st.write("GET response:", response)

    if response['status_code'] == 20000:
        task_status = response['tasks'][0]['status_message']
        st.write(f"Task status: {task_status}")  # Debugging line
        if task_status == "Task In Queue":
            st.write(f"Attempt {retry_count + 1}: Task is still in queue. Retrying in {WAIT_TIME} seconds...")
            retry_count += 1
            time.sleep(WAIT_TIME)
        elif task_status == "Ok.":  # Only set task_ready = True when the task is actually complete
            task_ready = True
            st.write("Task is ready.")  # Debugging line
    else:
        st.write(f"GET error. Code: {response['status_code']} Message: {response['status_message']}")
        break










