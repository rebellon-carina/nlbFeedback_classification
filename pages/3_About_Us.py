import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("We are a dynamic team dedicated to revolutionizing the way libraries categorize and deliver information. With the power of artificial intelligence and a passion for enhancing user experience, we’ve created a platform that transforms feedback into intuitive categories")

with st.expander("How to use this App"):
    st.write("1. Enter your feeback in the text area.")
    st.write("2. Click the 'Submit' button.")
    st.write("3. The app will generate the catergory  based on your prompt.")

st.write('*A POC project by CHR and GJ of NLB*')
