import streamlit as st
import client
from client import RestClient
import pandas as pd
import time
import re
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread

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
    conn = connect(credentials=credentials)
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    
    # Open the Google Sheet
    sheet_id = sheet_url.split('/')[-2]
    sh = gc.open_by_key(sheet_id)
    
    # Create a new worksheet with the given name
    worksheet = sh.add_worksheet(title=worksheet_name, rows="1000", cols="50")
    
    # Clear existing data if any (should be empty since it's a new worksheet)
    worksheet.clear()
    
    # Add new data
    worksheet.insert_rows(df.values.tolist(), row=1)
    
    # Add header
    worksheet.insert_row(df.columns.tolist(), index=1)
    
    st.success(f"Data successfully saved to a new worksheet named '{worksheet_name}' in the Google Sheet.")


st.title("Google Ads keywords for site")

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

target = st.text_input('Target domain', 'ashleystewart.com')
location_name = st.text_input('Location name', 'United States')
sheet_url = st.text_input('Sheet url', "https://docs.google.com/spreadsheets/d/1pe-M1yQ4jPP8jlH7Hadw1Xkc9KZo2PRTKwaYTnrKxsI/edit#gid=0")
new_worksheet_name = st.text_input("New worksheet name", "Keywords for site")

if st.button('Get data'):
    with st.status("Sending a POST request...") as status:
        post_data = dict()
        # simple way to set a task
        post_data[len(post_data)] = dict(
        location_name="United States",
        target="ashleystewart.com")

        response = client.post("/v3/keywords_data/google_ads/keywords_for_site/live", post_data)

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

# EXTRACT
def extract_product_details_from_response(response):
    all_products = []

    # Directly accessing the location of results based on the structure of your response
    items = response["tasks"][0]["result"]
    print(items)

    for item in items:
        product_info = {
            "keyword": item["keyword"],
            "location_code": item["location_code"],
            "language_code": item["language_code"],
            "search_partners": item["search_partners"],
            "competition": item["competition"],
            "competition_index": item["competition_index"],
            "search_volume": item["search_volume"],
            "low_top_of_page_bid": item["low_top_of_page_bid"],
            "high_top_of_page_bid": item["high_top_of_page_bid"]
            # "type": item["keyword_annotations"]["concepts"][1]["concept_group"]["type"]


        }
        # Adding the 'concept_name' and 'concept_type' based on the new rule
        concepts = item.get("keyword_annotations", {}).get("concepts", [])
        for concept in concepts:
            concept_type = concept.get("concept_group", {}).get("type", None)
            if concept_type in ["NON_BRAND", "BRAND"]:
                product_info["concept_name"] = concept.get("name", None)
                product_info["concept_type"] = concept_type
                break  # Exit the loop once a matching concept is found

        all_products.append(product_info)
        

    return all_products

# Usage
products = extract_product_details_from_response(response)
print(products)  # This should print the details of the first product

st.success("Success!")
df = pd.DataFrame.from_dict(products)
csv = df.to_csv(index=False)  # Convert the dataframe to CSV string format
st.write(df)
status.update(label="Data extracted!", state="complete", expanded=True)

st.download_button(
    label="Press to Download",
    data=csv,
    file_name="google-reviews.csv",
    mime="text/csv",
    key='download-csv'
)

save_to_new_worksheet(df, sheet_url, new_worksheet_name)