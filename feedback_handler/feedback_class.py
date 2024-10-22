import os
import json
import openai
from helper_functions import llm

# Load the JSON file
filepath = './data/feedback_mockdata.json'
with open(filepath, 'r') as file:
    json_string = file.read()
    dict_of_feedback = json.loads(json_string)
    print()


def identify_category(user_message):
    delimiter = "####"

    system_message = f"""
    You are tasked with categorizing customer feedback for a library\
    The feedback will be enclosed within four hashes, {delimiter}.

    Decide if the feedback is relevant to any predefined categories and subcategories
    in the Python dictionary below: 

    {dict_of_feedback}

    Think step by step. You may assign a piece of feedback to a category first before finding a suitable subcategory.
    Try to find and assign the best match that is closest to the predefined categories, you can assign 
    the subcategory to "Others" if there are no relevant subcategory.
    You may assign multiple categories and subcategories to a single piece if appropriate, 
    but ensure there are no duplicated subcategories for the same feedback. 
    For each category and subcategory assigned, identify and extract relevant keywords or phrases from the feedback 
    that justify the categorization. ONLY include keyword that provided in the given feedback below. 
    
    Output should be in the same format as the json data provided above excluding the feedback key 
    but include the key keywords where the value is a list of the extracted keywords.
    It should be a valid json, do not include the word json or backtick.
    Review if the json has duplicate Category and Subcategory, combine keywords for the same Category and Subcategory.  
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    feedback_category = llm.get_completion_by_messages(messages)
    return feedback_category


def process_feedback_class(user_input):
    delimiter = "```"
    return identify_category(user_input)
   