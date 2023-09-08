import streamlit as st
import client
from client import RestClient
import pandas as pd
import time

client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

st.title("🏠 Home")
st.text("Some intro and instructions here")



