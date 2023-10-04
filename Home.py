import streamlit as st
import client
from client import RestClient
import pandas as pd
import time

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

st.title("Smoke Finder💨")
txt = '''1. If You want to save data to Google Sheets, create a new spreadsheet  and share it with the service account email address: streamlit@mta-digital-bi.iam.gserviceaccount.com
2. You can change the suggested 'New worksheet name', but when fetching data back from sheets to the 'Summary' tab, the original name will be used.
3. When trying to save data to a new worksheet, make sure the worksheet name is unique.
4. If something doesn't work, :sob::sob::sob:
let him
:point_right::point_right::point_right: mateusz.bortnik@mta.digital :point_left::point_left::point_left:
know immediately.
'''
st.markdown(txt)

st.header("Roadmap")
st.markdown("1. Retreive reviews data from Yelp, Trustpilot, Google, Tripadvisor and Yelp and save them to Google Sheets")
st.markdown(":green[Done]")
st.markdown("2. Reconstruct reports similar to those in Ahrefs/Semrush")
st.markdown(":yellow[In progress]")
st.markdown("3. Build a summary page that will visualize the data from all sources and draw insights with GPT model")
st.markdown(":yellow[In progress]")
