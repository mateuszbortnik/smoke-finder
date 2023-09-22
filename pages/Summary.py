import streamlit as st
import client
from client import RestClient
import pandas as pd
import time
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread

def fetch_all_data_from_worksheets(sheet_url):
    # Initialize the dictionary to hold DataFrames
    dfs = {}
    
    try:
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
        
        # Get a list of all worksheets
        all_worksheets = sh.worksheets()
        
        # Get names of all worksheets
        worksheet_names = [ws.title for ws in all_worksheets]
        
        for worksheet_name in worksheet_names:
            # Open worksheet by name
            worksheet = sh.worksheet(worksheet_name)
            
            # Fetch all values
            values = worksheet.get_all_values()
            
            # Create a DataFrame
            df = pd.DataFrame(values[1:], columns=values[0])
            
            # Store in the dictionary
            dfs[worksheet_name] = df
        
        st.success("Data successfully fetched from all worksheets in the Google Sheet.")
        
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        
    return dfs


sheet_url = st.text_input('Sheet url', "https://docs.google.com/spreadsheets/d/1pe-M1yQ4jPP8jlH7Hadw1Xkc9KZo2PRTKwaYTnrKxsI/edit#gid=0")


data_frames = fetch_all_data_from_worksheets(sheet_url)

