import streamlit as st
import client
from client import RestClient
import pandas as pd
import time
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
    try:
        # Replace NaN values with a placeholder string (you can also use df.fillna(0) to replace with zero)
        df.fillna("NaN", inplace=True)

        # Replace Inf and -Inf with placeholder strings
        df.replace([float('inf'), float('-inf')], ["Inf", "-Inf"], inplace=True)

        # Connect to Google Sheets
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])

        # Open the Google Sheet
        sheet_id = sheet_url.split('/')[-2]
        sh = gc.open_by_key(sheet_id)

        # Create a new worksheet with the given name
        worksheet = sh.add_worksheet(title=worksheet_name, rows="1000", cols="50")

        # Clear existing data if any (should be empty since it's a new worksheet)
        worksheet.clear()

        # Add header
        worksheet.insert_row(df.columns.tolist(), index=1)

        # Add new data
        for i, value in enumerate(df.values.tolist()):
            worksheet.insert_row(value, index=i + 2)
        
        st.success(f"Data successfully saved to a new worksheet named '{worksheet_name}' in the Google Sheet.")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

st.title("Google Trends")

# post_data = dict()
# # simple way to set a task
# post_data[len(post_data)] = dict(
#     location_name="United States",
#     date_from="2019-01-01",
#     date_to="2020-01-01",
#     keywords=[
#         "seo api"
#     ]
# )

# response = client.post("/v3/keywords_data/google_trends/explore/task_post", post_data)

# if response["status_code"] == 20000:
#     st.write("POST response:", response)
#     task_id = response["tasks"][0]["id"]
#     print("Task ID:", task_id)
# else:
#     print(f"POST error. Code: {response['status_code']} Message: {response['status_message']}")
#     st.stop()

#     # Wait a few seconds before checking task status
# time.sleep(2)

WAIT_TIME = 10
task_ready = False
task_id='09271218-6487-0170-0000-bb7e2fe0ff5d'
while not task_ready:
    # st.write(f"Retry count: {retry_count}")  # Debugging line
    response = client.get(f"/v3/keywords_data/google_trends/explore/task_get/{task_id}")
    st.write("GET response:", response)

    if response['status_code'] == 20000:
        task_status = response['tasks'][0]['status_message']
        st.write(f"Task status: {task_status}")  # Debugging line
        if task_status == "Task In Queue":
            # st.write(f"Attempt {retry_count + 1}: Task is still in queue. Retrying in {WAIT_TIME} seconds...")
            
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
        items = response["tasks"][0]["result"][0]["items"][0]["data"]
        st.write("ITEMS HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")
        st.write(items)

        for item in items:
            product_info = {
                    "date_from": item["date_from"],
                    "date_to": item["date_to"],
                    "values": item["values"]
                }
            all_products.append(product_info)

        return all_products

    # # Usage
    products = extract_product_details_from_response(response)
    print(products)  # This should print the details of the first product

    # st.success("Success!")
    df = pd.DataFrame.from_dict(products)
    st.write(df["values"].dtype)
    # csv = df.to_csv(index=False)  # Convert the dataframe to CSV string format
    st.write(df)