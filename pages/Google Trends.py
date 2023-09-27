import streamlit as st
import client
from client import RestClient
import pandas as pd
import time
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread
from pytrends.request import TrendReq

pytrend = TrendReq()

#provide your search terms
kw_list=['Facebook', 'Apple', 'Amazon', 'Netflix', 'Google']

historicaldf = pytrend.get_historical_interest(kw_list, year_start=2020, month_start=10, day_start=1, hour_start=0, year_end=2021, month_end=10, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
st.dataframe(historicaldf)