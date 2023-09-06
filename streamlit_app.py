import streamlit as st
import client
from client import RestClient
import pandas as pd
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
    # after a task is completed, we will send a GET request to the address you specify
    # instead of $id and $tag, you will receive actual values that are relevant to this task
    post_data[len(post_data)] = dict(
        domain=domain,
        depth=100,
        # priority=2,
        # tag="some_string_123",
        pingback_url="https://your-server.com/pingscript?id=$id&tag=$tag"
    )
    # after a task is completed, we will send a GET request to the address you specify
    # instead of $id and $tag, you will receive actual values that are relevant to this task
    post_data[len(post_data)] = dict(
        domain=domain,
        postback_url="https://your-server.com/postbackscript"
    )
    # POST /v3/business_data/trustpilot/reviews/task_post
    response = client.post("/v3/business_data/trustpilot/reviews/task_post", post_data)
    # you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
    if response["status_code"] == 20000:
        print(response)
        # do something with result
    else:
        print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

    # st.write(response)

    #GET
    response = client.get("/v3/business_data/trustpilot/reviews/tasks_ready")
    # you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
    if response['status_code'] == 20000:
        results = []
        tasks = response['tasks']
        if tasks:  # Check if the list is not empty
            last_task = tasks[0]  # Get the last task
            if last_task['result'] and len(last_task['result']) > 0:
                for resultTaskInfo in last_task['result']:
                    if resultTaskInfo['id']:
                        results.append(client.get("/v3/business_data/trustpilot/reviews/task_get/" + resultTaskInfo['id']))
                        
        print(results)
        # do something with result
    else:
        print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))



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
                    items = result_data[-1]["items"]
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


