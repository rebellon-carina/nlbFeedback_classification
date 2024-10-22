import streamlit as st
import pandas as pd
import json


# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Data"
)
# endregion <--------- Streamlit App Configuration --------->

# Load the JSON file
filepath = './data/feedback_mockdata.json'
with open(filepath, 'r') as file:
    json_string = file.read()
    dict_of_feedback = json.loads(json_string)
   
# display the `dict_of_course` as a Pandas DataFrame
df = pd.DataFrame(dict_of_feedback['feedback_data'])


#st.write(df)
df = df.rename(columns={"category": "Category", "subcategory": "Subcategory", "feedback": "Feedback"})
st.markdown(df.to_html(escape=False, index=False, justify="center"), unsafe_allow_html=True)