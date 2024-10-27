import streamlit as st
from test_data_and_functions import cleaning_output
import pandas as pd
from utility import check_password

if not check_password():  
    st.stop()

st.title("Validation Test Set")
st.write("This page displays the validation test set for the classification model. "
         "The test set was consonlidated from CRM feedback from 2021 and some manually categorised CSS feedback for categories that did not exist in 2021.")

test_data = pd.read_csv("test_data_and_functions/Composite test set for all categories.csv")
validation_results = pd.read_csv("test_data_and_functions/validation_results.csv")
validation_cat = validation_results.drop_duplicates(["Cleaned Text", "Category", "correct_cat_flag"])
total_count = test_data.shape[0]

if test_data is not None and not test_data.empty:
    # Display the data in an interactive table
    st.dataframe(test_data)
else: 
    st.write("No test data available")

if validation_results is not None and not validation_results.empty:
    st.subheader("Validation Summary")
    # recall for categories: number of correctly classified categories out of test set
    st.write(f"Number of correct categories: {validation_cat["correct_cat_flag"].sum()} of {total_count}")
    # recall for sub-categories.
    st.write(f"Number of correct sub-categorisations: {validation_results["correct_sub_cat_flag"].sum()} of {total_count}")
else:
    st.write("No validation results available.")