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
max_crawl_pages = st.text_input('Max crawl pages', '10')
if st.button('Get data'):
    rnd = Random()
    post_data = dict()

    post_data[rnd.randint(1, 30000000)] = dict(
        target=target,
        max_crawl_pages=max_crawl_pages
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

    WAIT_TIME = 10

    task_ready = False
    crawl_ready=False
    while not task_ready or not crawl_ready:
        # st.write(f"Retry count: {retry_count}")  # Debugging line
        response = client.get(f"/v3/on_page/summary/{task_id}")
        # st.write("GET response:", response)

        if response['status_code'] == 20000:
            task_status = response['tasks'][0]['status_message']
            # st.write(f"Task status: {task_status}")  # Debugging line
            if task_status == "Task In Queue":
                st.write(f"Attempt Task is still in queue. Retrying in {WAIT_TIME} seconds...")
                
                time.sleep(WAIT_TIME)
            elif task_status == "Ok.": # Only set task_ready = True when the task is actually complete
                task_ready = True
                # st.write("Task is ready.")  # Debugging line
                # st.write("GET response:", response)
                crawl_status = response['tasks'][0]['result'][0]['crawl_progress']
                # st.write(crawl_status)
                if crawl_status == "in_progress":
                        time.sleep(WAIT_TIME)
                elif crawl_status == "finished":
                        crawl_ready = True
                        # st.write("crawl ready GET response:", response)
        else:
            st.write(f"GET error. Code: {response['status_code']} Message: {response['status_message']}")
            break



# EXTRACT

    data = response["tasks"][0]

    # Recursive function to flatten nested dictionaries
    def flatten_dict(d, parent_key='', sep='_'):
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items

    # Apply the flatten_dict function to each item in the result list
    flattened_data = [flatten_dict(item) for item in data['result']]

    # Convert to DataFrame
    df = pd.DataFrame(flattened_data)
    df = df.melt(var_name='Attribute', value_name='Value')
    # Display the DataFrame
    print(df)


    st.success("Success!")

    csv = df.to_csv(index=False)  # Convert the dataframe to CSV string format
    st.write(df)

    st.download_button(
        label="Press to Download",
        data=csv,
        file_name="trustpilot-reviews.csv",
        mime="text/csv",
        key='download-csv'
    )






