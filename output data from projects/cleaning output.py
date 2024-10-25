import pandas as pd
from feedback_handler import feedback_class
import json
import re
import matplotlib.pyplot as plt
import time
import numpy as np

# read test data
test_data = pd.read_csv("output data from projects/Composite test set for all categories.csv")

# run through model
def iterate_test_set(test_data):
    # Record the start time
    start_time = time.time()
    print("Starting the function...")

    # Extract the "Cleaned Text" data
    feedback = test_data["Cleaned Text"]
    classified = []

    # Process each user message
    for user_message in feedback:
        response = feedback_class.process_feedback_class(user_message) 
        try:
            response_json = json.loads(response)
            responses = response_json.get("feedback_data")
            for response_dict in responses:
                response_dict["feedback_text"] = user_message
                classified.append(response_dict)
            
        except:
            classified.append({"category":"","subcategory":"", 
                               "keywords": "", "feedback_text":user_message})
    # Convert the list of responses to a DataFrame
    df = pd.json_normalize(classified)

    # Record the end time and calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print the elapsed time in a readable format
    print(f"Function completed in {elapsed_time:.2f} seconds.")
    
    return df, classified

df, classified = iterate_test_set(test_data)
# showed there was a difference between the feedback in the input and output, making it difficult for matching

# check =[]
# for i in range(len(test_data["Cleaned Text"][0])):
#     check.append(test_data["Cleaned Text"][0][i] == output.feedback[0][i])
# test_data["Cleaned Text"][0]== output.feedback[0]

# Remove trailing new line in output to match with input
# df["feedback_cleaned"] = df["feedback_text"].apply(lambda x: x.replace("\n", ""))
# output.to_csv("2024-10-20T11-14_export_cleaned.csv")

# change Physical and Digital collection to Collection-Print and Collection-e
validation = test_data.merge(df, how = "left", left_on = "Cleaned Text", right_on = "feedback_text", suffixes = (None, "_output"))
# validation[["Cleaned Text", "feedback_cleaned"]].head()
# validation["category"].replace("Physical Collection", "Collection-Print", inplace = True)
# validation["category"].replace("Digital Collection", "Collection-e", inplace = True)

# create a combination field for category and sub category
validation["comb_cat"] = validation["Category"] + validation["Sub Category"]
validation["comb_cat_output"] = validation["category"] + validation["subcategory"]

validation[["Cleaned Text","feedback","comb_cat", "comb_cat_output"]].iloc[1]

correct_sub_cat = validation["comb_cat"] == validation["comb_cat_output"] 
correct_cat = validation["Category"] == validation["category"] 

validation["correct_cat"] = correct_cat
validation["correct_sub_cat"] = correct_sub_cat

# keep only unique categories for each feedback in test set
validation_cat = validation.drop_duplicates(["Cleaned Text", "Category", "correct_cat"])

# recall for categories: number of correctly classified categories out of test set
print(f"Number of correct categories: {sum(validation_cat["correct_cat"])} of {test_data.shape[0]}")
# recall for sub-categories.
print(f"Number of correct sub-categorisations: {sum(correct_sub_cat)} of {test_data.shape[0]}")

validation.to_csv("validation_results.csv")