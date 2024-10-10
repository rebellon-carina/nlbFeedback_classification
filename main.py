# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from feedback_handler import feedback_class
import json
import plotly.express as px
from utility import check_password
import re
from io import StringIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
import numpy as np
from PIL import Image

#debugging 
debug = 0

if not check_password():  
    st.stop()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Feedback Categorization POC"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Feedback Entry Form")

if 'df_feedback' not in st.session_state:
    st.session_state.df_feedback = pd.DataFrame()

if 'df_feedback_unknown' not in st.session_state:
    st.session_state.df_feedback_unknown = pd.DataFrame()

if 'record_ctr' not in st.session_state:
    st.session_state.record_ctr = 0

if 'all_feedback' not in st.session_state:
    st.session_state.all_feedback = "NLB"

# Function to parse the pasted text
def parse_records(input_text):
    # Split the input text by double quotes and filter out empty strings
   #records = [record.strip() for record in input_text.split('"') if record.strip()]
    

    pattern = r'(?:[^"\n]+|"[^"]*")+(?:\n|$)'
    records = re.findall(pattern, input_text)

    # Filter out any empty strings that may occur due to split
    return [record for record in records if record]


form = st.form(key="form")
#form.subheader("Prompt")

user_prompt = form.text_area("Enter your feeback here, you can copy multiple feedback from excel and paste it here. Records will be split by double quotes or new line.", height=400)

if form.form_submit_button("Submit"):
        
    st.toast(f"User Input Submitted - {user_prompt}")
    records = parse_records(user_prompt)
    
    iterations = len(records)

    progress_bar = st.progress(0)
    counter = st.empty()  # Placeholder for the counter
    timer = st.empty()    # Placeholder for the timer
    start_time = time.time()  # Start the timer

    i=0

    for  record in records:
        st.session_state.all_feedback += record
        st.session_state.record_ctr += 1

        
        progress_percentage = (i + 1) / iterations
        progress_bar.progress(progress_percentage)  # Update the progress bar
        counter.text(f"Current Count: {i + 1} / {iterations} ")  # Update the dynamic counter
        i += 1

        # Update the timer
        elapsed_time = time.time() - start_time
        timer.text(f"Elapsed Time: {int(elapsed_time)} seconds")

        if debug == 1:
            st.write(f"Debug Record :{record}")

        response= feedback_class.process_feedback_class(record)
                     
        if debug == 1:
            st.write(f"Debug Response :{response}")


        try:
            response_json = json.loads(response)

            df = pd.DataFrame(response_json['feedback_data'])
            df['feedback'] = record
            
            if(len(df) > 0):

                if(len(st.session_state.df_feedback) > 0):
                    st.session_state.df_feedback = pd.concat([st.session_state.df_feedback, df], ignore_index=True)
                    
                else:
                    st.session_state.df_feedback = df
            else:
                
                df = pd.DataFrame({'Feeedback': [record]})

                if(len(st.session_state.df_feedback_unknown) > 0):  
                    st.session_state.df_feedback_unknown = pd.concat([st.session_state.df_feedback_unknown, df], ignore_index=True)
                else:
                    st.session_state.df_feedback_unknown = df
        except:

            df = pd.DataFrame({'Feeedback': [record]})

            if(len(st.session_state.df_feedback_unknown) > 0):  
                st.session_state.df_feedback_unknown = pd.concat([st.session_state.df_feedback_unknown, df], ignore_index=True)
            else:
                st.session_state.df_feedback_unknown = df
    
    st.success("Process completed!")
    total_time = int(time.time() - start_time)
    st.write(f"Total Duration: {total_time} seconds")

    st.markdown(f"""
                        | :blue[No of Feedback Processed] | :red[No of Feedback without Category]    |
                        |-----------------------------------|------------------------------------------|
                        | {st.session_state.record_ctr}        |  {len(st.session_state.df_feedback_unknown)} |""")
    
    st.write("With Category")
    st.write(st.session_state.df_feedback)

    st.divider()

    if(len(st.session_state.df_feedback_unknown) > 0):
        st.write("Without Category")
        st.write(st.session_state.df_feedback_unknown)
        st.divider()


    # Create a stacked bar chart

    df_count = st.session_state.df_feedback.groupby(['category', 'subcategory']).size().reset_index(name='count')

    # Create a stacked bar chart
    fig = px.bar(df_count, 
                x='category', 
                y='count', 
                color='subcategory', 
                title='Feedback by Category and SubCategory (Count)',
                labels={'count': 'count', 'category': 'category'},
                text='count')

    # Update layout for better readability
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(barmode='stack')

    st.plotly_chart(fig)


    st.markdown("""
        <style>
        .title {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }
        </style>
        <div class="title">WordCloud from Feedback</div>
        """,
        unsafe_allow_html=True
    )

    # Create and generate a word cloud image:
    book_mask = np.array(Image.open('image/book_mask.png'))

    wordcloud = WordCloud(width=800, height=400, background_color='white',#mask=book_mask,
                            contour_color='black', contour_width=1).generate(st.session_state.all_feedback)
    
    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Hide the axes
    plt.tight_layout()

    # Show the plot in Streamlit
    st.pyplot(plt)