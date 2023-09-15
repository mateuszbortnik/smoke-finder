import streamlit as st
import client
from client import RestClient
import pandas as pd
import time

st.title("Content Analysis")

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

keyword = st.text_input('Keyword', 'Ashley Stewart')

if st.button('Get data'):
    post_data = dict()
    # simple way to set a task
    post_data[len(post_data)] = dict(keyword=keyword)

    response = client.post("/v3/content_analysis/search/live", post_data)

    if response["status_code"] == 20000:
        # st.write("POST response:", response)
        task_id = response["tasks"][0]["id"]
        print("Task ID:", task_id)
    else:
        print(f"POST error. Code: {response['status_code']} Message: {response['status_message']}")
        st.stop()

        # Wait a few seconds before checking task status
    time.sleep(2)


        # EXTRACT
    def extract_product_details_from_response(response):
        all_products = []

        # Directly accessing the location of results based on the structure of your response
        items = response["tasks"][0]["result"][0]["items"]

        for item in items:
            product_info = {
                "url": item["url"],
                "fetch_time": item["fetch_time"],
                "country": item["country"],
                "score": item["score"],
                "content_type": item["content_info"]["content_type"],
                "title": item["content_info"]["title"],
                "snippet": item["content_info"]["snippet"],
                "anger": item["content_info"]["sentiment_connotations"]["anger"],
                "happiness": item["content_info"]["sentiment_connotations"]["happiness"],
                "love": item["content_info"]["sentiment_connotations"]["love"],
                "sadness": item["content_info"]["sentiment_connotations"]["sadness"],
                "share": item["content_info"]["sentiment_connotations"]["share"],
                "fun": item["content_info"]["sentiment_connotations"]["fun"],
                "positive": item["content_info"]["connotation_types"]["positive"],
                "negative": item["content_info"]["connotation_types"]["negative"],
                "neutral": item["content_info"]["connotation_types"]["neutral"],
                "date_published": item["content_info"]["date_published"],
                "content_quality_score": item["content_info"]["content_quality_score"]
            }
            all_products.append(product_info)

        return all_products

        # Usage
    products = extract_product_details_from_response(response)
    print(products)  # This should print the details of the first product
    df = pd.DataFrame.from_dict(products)
    st.dataframe(df)
    csv = df.to_csv(index=False)  # Convert the dataframe to CSV string format
   

    st.download_button(
        label="Press to Download",
        data=csv,
        file_name="content-analysis.csv",
        mime="text/csv",
        key='download-csv'
    )