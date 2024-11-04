import streamlit as st
import pandas as pd
import json
from utility import check_password

if not check_password():  
    st.stop()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Data"
)
# endregion <--------- Streamlit App Configuration --------->

# Load the JSON file
filepath = './data/combined_feedback.json'
with open(filepath, 'r') as file:
    json_string = file.read()
    dict_of_feedback = json.loads(json_string)
   
# display the `dict_of_course` as a Pandas DataFrame
df = pd.DataFrame(dict_of_feedback)


#st.write(df)
df = df.rename(columns={"category": "Category", "subcategory": "Subcategory", "feedback": "Feedback"})
st.markdown(df.to_html(escape=False, index=False, justify="center"), unsafe_allow_html=True)