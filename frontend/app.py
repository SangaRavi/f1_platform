# =========================================
# H2O AutoML Training with MLflow Tracking
# Author: Kenneth Leung
# Last Modified: 30 May 2022
# =========================================
# Command to execute script locally: streamlit run app.py
# Command to run Docker image: docker run -d -p 8501:8501 <streamlit-app-name>:latest

import streamlit as st
import requests


endpoint = 'http://host.docker.internal:8000/v1/visualizations'  # Specify this path for Dockerization to work


st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon='✅',
    layout='wide'
)

st.sidebar.title("Select Session")
year = st.sidebar.selectbox(
    "Choose Year",
    (2023, 2022)
)

country = st.sidebar.selectbox(
    "Choose Country",
    ("Spain", "Monaco")
)

mode = st.sidebar.selectbox(
    "Choose Mode",
    ("R","Q")
)
# dashboard title

ingest = st.selectbox("Select data ingestion category: ", ("lapgaps",))

if st.button("submit"):
    if ingest == "lapgaps":
        output = requests.get(endpoint, timeout=8000)
        st.subheader(output)

