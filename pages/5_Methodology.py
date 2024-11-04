import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Methodology"
)

st.subheader("Brief Notes")
st.write("""
         This app was designed to be used on GSIB. It accesses GovTech's GovText and Cloak API.
         After a user copies and pastes the feedback from Excel and submits it, 
         the app seperates the rows of feedback before sending each feedback individually to an LLM for classification. 
         The user will subsequently download and transform the data outside of the app. 
         """)

st.subheader("Flow Chart")
st.image("pages/Flow_Diagram.png")