import streamlit as st
import client
from client import RestClient
import pandas as pd
import time
import re
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread
from pandas import json_normalize

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

def save_to_new_worksheet(df, sheet_url, worksheet_name):
    # Connect to Google Sheets
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )

    try:
        conn = connect(credentials=credentials)
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        
        # Open the Google Sheet
        sheet_id = sheet_url.split('/')[-2]
        sh = gc.open_by_key(sheet_id)
        
        # Create a new worksheet with the given name
        worksheet = sh.add_worksheet(title=worksheet_name, rows="10000", cols="500")
        
        # Clear existing data if any (should be empty since it's a new worksheet)
        worksheet.clear()
        
        # Add new data
        df=df.fillna('')
        worksheet.insert_rows(df.values.tolist(), row=1, value_input_option='USER_ENTERED')
        
        # Add header
        worksheet.insert_row(df.columns.tolist(), index=1)

        problematic_value = df.iloc[0, 13]
        st.write("Problematic Value:", problematic_value)
        st.write("Data Type:", type(problematic_value))
        
        st.success(f"Data successfully saved to a new worksheet named '{worksheet_name}' in the Google Sheet.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.title("Domain Intersection")
st.markdown('''This endpoint will provide you with the keywords for which both specified domains rank within the same SERP. You will get search volume, competition, cost-per-click and impressions data on each intersecting keyword. Along with that, you will get data on the first and second domain’s SERP element discovered for this keyword, as well as the estimated traffic volume and cost of ad traffic. Domain Intersection endpoint supports organic, paid, local pack, and featured snippet results.
            
Fields descriptions and more: https://docs.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live/?python           ''')
client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

target1 = st.text_input('Target domain 1', 'ashleystewart.com', key='target1')
target2 = st.text_input('Target domain 2', 'fashionnova.com', key='target2')
location_name = st.text_input('Location name', 'United States')
sheet_url = st.text_input('Sheet url', "https://docs.google.com/spreadsheets/d/1pe-M1yQ4jPP8jlH7Hadw1Xkc9KZo2PRTKwaYTnrKxsI/edit#gid=0")
new_worksheet_name = st.text_input("New worksheet name", "Domain Intersection")

if st.button('Get data'):
    with st.status("Sending a POST request...") as status:
        post_data = dict()
        # simple way to set a task
        post_data[len(post_data)] = dict(
            target1=target1,
            target2=target2,
            location_name=location_name,
            language_name="English",

        )

        response = client.post("/v3/dataforseo_labs/google/domain_intersection/live", post_data)

        if response["status_code"] == 20000:
            st.write("POST response:", response)
            task_id = response["tasks"][0]["id"]
            print("Task ID:", task_id)
            status.update(label="Task ready!", state="complete")
        else:
            print(f"POST error. Code: {response['status_code']} Message: {response['status_message']}")
            st.stop()

            # Wait a few seconds before checking task status
        time.sleep(2)

    with st.status("Extracting data...") as status:
    # EXTRACT
        def extract_product_details_from_response(response):
            items_data = response['tasks'][0]['result'][0]['items']
            df_items = json_normalize(items_data)
            return df_items
                        


            # Usage
        products = extract_product_details_from_response(response)


        st.success("Success!")
        df = pd.DataFrame.from_dict(products)
        df = df.loc[:, ~df.columns.isin(['keyword_data.keyword_info.monthly_searches', 'keyword_data.keyword_info.categories', 'first_domain_serp_element.extended_snippet'])]
        csv = df.to_csv(index=False)  # Convert the dataframe to CSV string format
        st.write(df)
        st.write(df.dtypes)
        status.update(label="Data extracted!", state="complete", expanded=True)

    st.download_button(
        label="Press to Download",
        data=csv,
        file_name="domain-intersection.csv",
        mime="text/csv",
        key='download-csv'
    )

    save_to_new_worksheet(df, sheet_url, new_worksheet_name)