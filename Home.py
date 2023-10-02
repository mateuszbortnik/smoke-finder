import streamlit as st
import client
from client import RestClient
import pandas as pd
import time

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

st.title("Smoke Finder💨")
st.text("1. In order to save data to Google Sheets, create a new spreadsheet and share it with the service account email address: streamlit@mta-digital-bi.iam.gserviceaccount.com")



