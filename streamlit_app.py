import streamlit as st
import client
from client import RestClient
import pandas as pd
import time

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

st.title("Trustpilot reviews")
domain = st.text_input('Domain', 'www.ashleystewart.com')

if st.button('Get data'):
    # POST request to enqueue a task
    post_data = dict()
    post_data[len(post_data)] = dict(domain=domain)
    response = client.post("/v3/business_data/trustpilot/reviews/task_post", post_data)

    if response["status_code"] == 20000:
        st.write("POST response:", response)
        task_id = response["tasks"][0]["id"]
        st.write("Task ID:", task_id)
    else:
        st.write(f"POST error. Code: {response['status_code']} Message: {response['status_message']}")
        st.stop()

    # Wait a few seconds before checking task status
    time.sleep(2)

    # GET request to fetch the results of the task
    MAX_RETRIES = 100000
    WAIT_TIME = 10
    retry_count = 0
    task_ready = False

    while retry_count < MAX_RETRIES and not task_ready:
        response = client.get(f"/v3/business_data/trustpilot/reviews/task_get/{task_id}")
        st.write("GET response:", response)

        if response['status_code'] == 20000:
            task_status = response['tasks'][0]['status_message']
            if task_status == "Task In Queue":
                st.write(f"Attempt {retry_count + 1}: Task is still in queue. Retrying in {WAIT_TIME} seconds...")
                retry_count += 1
                time.sleep(WAIT_TIME)
            else:
                task_ready = True
        else:
            st.write(f"GET error. Code: {response['status_code']} Message: {response['status_message']}")
            st.stop()

    if task_ready:
        # Extract and display results
        results = response['tasks'][0].get('result', [])
        st.write("Results:", results)
    else:
        st.write("Task not ready after maximum retries.")
        st.stop()

    # Further processing, if needed
    # ...




    #EXTRACT
    def extract_product_details_from_list(results):
        all_products = []

        for result in results:
            tasks = result.get("tasks", [])

            for task in tasks:
                result_data = task.get("result", {})

                if isinstance(result_data, dict) and "items" in result_data:
                    items = result_data["items"]
                elif isinstance(result_data, list) and "items" in result_data[0]:
                    items = result_data[0]["items"]
                else:
                    items = []

                for item in items:



                    product_info = {
                            "rating": item["rating"]["value"],
                            "timestamp": item["timestamp"],
                            "review_text": item["review_text"]
                        }
                    all_products.append(product_info)

        return all_products

    # Usage
    products = extract_product_details_from_list(results)
    print(products)  # This should print the details of the first product

    st.success("Success!")
    df = pd.DataFrame.from_dict(products)
    df.to_csv("reviews.csv")
    df


