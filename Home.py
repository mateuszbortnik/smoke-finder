import streamlit as st
import client
from client import RestClient
import pandas as pd
import time

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

st.title("Smoke Finder💨")
txt = '''1. If You want to save data to Google Sheets, create a new spreadsheet  and share it with the service account email address: streamlit@mta-digital-bi.iam.gserviceaccount.com
2. You can change the suggested 'New worksheet name', but when fetching data back from sheets to 'Summary' tab, the original name will be used.


'''
st.markdown(txt)



