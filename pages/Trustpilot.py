import streamlit as st
import client
from client import RestClient
import pandas as pd
import time
from google.oauth2 import service_account
from gsheetsdb import connect

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = "https://docs.google.com/spreadsheets/d/1pe-M1yQ4jPP8jlH7Hadw1Xkc9KZo2PRTKwaYTnrKxsI/edit#gid=0"
rows = run_query(f'SELECT * FROM "{sheet_url}"')

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

st.title("Trustpilot reviews")
domain = st.text_input('Domain', 'www.ashleystewart.com')

if st.button('Get data'):
    # POST request to enqueue a task
    post_data = dict()
    post_data[len(post_data)] = dict(domain=domain,depth=25000)
    response = client.post("/v3/business_data/trustpilot/reviews/task_post", post_data)

    if response["status_code"] == 20000:
        # st.write("POST response:", response)
        task_id = response["tasks"][0]["id"]
        # st.write("Task ID:", task_id)
    else:
        st.write(f"POST error. Code: {response['status_code']} Message: {response['status_message']}")
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
        response = client.get(f"/v3/business_data/trustpilot/reviews/task_get/{task_id}")
        # st.write("GET response:", response)

        if response['status_code'] == 20000:
            task_status = response['tasks'][0]['status_message']
            # st.write(f"Task status: {task_status}")  # Debugging line
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


        



    # EXTRACT
    def extract_product_details_from_response(response):
        all_products = []

        # Directly accessing the location of results based on the structure of your response
        items = response["tasks"][0]["result"][0]["items"]

        for item in items:
            product_info = {
                "rating": item["rating"]["value"],
                "timestamp": item["timestamp"],
                "review_text": item["review_text"]
            }
            all_products.append(product_info)

        return all_products

    # Usage
    products = extract_product_details_from_response(response)
    print(products)  # This should print the details of the first product

    st.success("Success!")
    df = pd.DataFrame.from_dict(products)
    csv = df.to_csv(index=False)  # Convert the dataframe to CSV string format
    st.write(df)

    st.download_button(
        label="Press to Download",
        data=csv,
        file_name="trustpilot-reviews.csv",
        mime="text/csv",
        key='download-csv'
    )



