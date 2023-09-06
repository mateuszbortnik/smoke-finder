import streamlit as st
import client
from client import RestClient
import pandas as pd
import time
client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

st.title("Trustpilot reviews")
domain = st.text_input('Domain', 'www.ashleystewart.com')

if st.button('Get data'):

    #POST
    post_data = dict()
    # simple way to set a task
    post_data[len(post_data)] = dict(
        domain=domain
    )

    # POST /v3/business_data/trustpilot/reviews/task_post
    response = client.post("/v3/business_data/trustpilot/reviews/task_post", post_data)
    # you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
    if response["status_code"] == 20000:
        print(response)
        # do something with result
    else:
        print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

    st.write(response)
    time.sleep(2)

    # Save the task ID from the POST request response
    task_id = response["tasks"][0]["id"]
    st.write(task_id)

    # GET
    response = client.get(f"/v3/business_data/trustpilot/reviews/task_get/{task_id}")
    st.write(response)
    # Check for successful response
    # Check for successful response
    if response['status_code'] == 20000:
        results = []  # Initialize or clear the results list
        
        # Safety check to ensure 'result' key exists and has data
        if 'result' in response and response['result'] and len(response['result']) > 0:
            for resultTaskInfo in response['result']:
                if resultTaskInfo['id'] == task_id:  # Check if the task ID matches
                    results.append(client.get(f"/v3/business_data/trustpilot/reviews/task_get/{task_id}"))

        print(results)
        # Do something with the result
    else:
        print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))



    st.write(results)


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


