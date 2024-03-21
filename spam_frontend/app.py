import streamlit as st
import json
import requests
url= "http://backend.docker:8000/predict"
header = {'Content-Type': 'application/json'}

st.set_page_config(page_title="Spam Classifier Front End")
st.title("Welcome to the Spam Classifier Dashboard")
st.write("Enter the Email you want to Predict")

email = st.text_input("Email to predict")

if st.button('Spam Classifier Prediction'):
    data = {"email": email}
    payload=json.dumps(data)
    response = requests.request("POST", url, headers=header, data=payload)
    response = response.text    
    st.write(f"The Email is {str(response)}")