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
from helper_functions import cloakapi
import matplotlib.lines as mlines

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



# try catch Cloak API
if 'df_cloak_available' not in st.session_state:
    try:
        response =  cloakapi.check_connection()

        if response.status_code >= 400 and response.status_code <= 600:
            st.session_state.df_cloak_available = 0
            st.markdown('### :heavy_exclamation_mark: :red[Cloak Anonymisation API Not Enabled. Do not submit if theres sensitive information]')
        else:
            st.session_state.df_cloak_available = 1
            st.markdown('### :white_check_mark: :blue[Cloak Anonymisation API Enabled]')
    except:
        st.session_state.df_cloak_available = 0
        st.markdown('### :heavy_exclamation_mark: :red[Cloak Anonymisation API Not Enabled. Do not submit if theres sensitive information]')
else:
    if st.session_state.df_cloak_available == 1:
        st.markdown('### :white_check_mark: :blue[Cloak Anonymisation API Enabled]')
    else:
        st.markdown('### :heavy_exclamation_mark: :red[Cloak Anonymisation API Not Enabled. Do not submit if theres sensitive information]')

# initialising dataframes to store output variables
if 'df_feedback' not in st.session_state: # can we remove this since the session_state.df_feedback is initiated again later?
    st.session_state.df_feedback = pd.DataFrame()

if 'df_feedback_unknown' not in st.session_state:
    st.session_state.df_feedback_unknown = 0

if 'record_ctr' not in st.session_state:
    st.session_state.record_ctr = 0

if 'all_feedback' not in st.session_state:
    st.session_state.all_feedback = "NLB"

# Function to parse the pasted text
def parse_records(input_text):
    # Split the input text by double quotes or new line and filter out empty strings

    pattern = r'(?:[^"\n]+|"[^"]*")+(?:\n|$)'
    records = re.findall(pattern, input_text)

    # Filter out any empty strings that may occur due to split
    return [record for record in records if record]

st.title(":pencil: Feedback Entry Form")

form = st.form(key="form")

# text box for users to input feedback texts by copying and pasting for excel
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

    # Loop through all feedback and send each piece of feedback to LLM for classification separately
    for record in records:
        st.session_state.all_feedback += record # append feedback that will eventually be printed in dataframe
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

        # cleaning with cloak before sending to LLM
        if st.session_state.df_cloak_available == 1:
            try:
                record = cloakapi.cloak_transform(record)
            except:
                st.write(f"Error in Text Anonymisation, unable to proceed {record}")
                break

        response= feedback_class.process_feedback_class(record) # send record to LLM to classify
                     
        if debug == 1:
            st.write(f"Debug Response :{response}")


        try: # check if LLM output is in suitable format
            response_json = json.loads(response)

            df = pd.DataFrame(response_json['feedback_data'])
            df['feedback'] = record
            
            if(len(df) > 0):

                if(len(st.session_state.df_feedback) > 0):
                    st.session_state.df_feedback = pd.concat([st.session_state.df_feedback, df], ignore_index=True)
                    
                else: 
                    st.session_state.df_feedback = df
            else:
                
                st.session_state.df_feedback_unknown += 1

                df = pd.DataFrame({'category':'Unknown', 'subcategory':'', 'keywords':[[]], 'sentiment': '', 'rating':'', 'feedback': [record]})

                if(len(st.session_state.df_feedback) > 0):
                    st.session_state.df_feedback = pd.concat([st.session_state.df_feedback, df], ignore_index=True)
                    
                else: 
                    st.session_state.df_feedback = df
        except: 
            st.session_state.df_feedback_unknown += 1

            df = pd.DataFrame({'category':'Unknown', 'subcategory':'', 'keywords':[[]], 'sentiment': '', 'rating':'', 'feedback': [record]})

            if(len(st.session_state.df_feedback) > 0):
                    st.session_state.df_feedback = pd.concat([st.session_state.df_feedback, df], ignore_index=True)        
            else: 
                    st.session_state.df_feedback = df
    
    st.success("Process completed!")
    total_time = int(time.time() - start_time)
    st.write(f"Total Duration: {total_time} seconds")

    st.markdown(f"""
                        | :blue[No of Feedback Processed] | :red[No of Feedback without Category]    |
                        |-----------------------------------|------------------------------------------|
                        | {st.session_state.record_ctr}        |  {st.session_state.df_feedback_unknown} |""")
    
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")
    
    @st.fragment()
    def download_button():
        st.download_button( # download button to faciliate download on GSIB
            label="Download data as CSV",
            data=convert_df(st.session_state.df_feedback),
            file_name="large_df.csv",
            mime="text/csv"
            )

    if(len(st.session_state.df_feedback) > 0):
        st.write("Feedback Category/Subcategory with Ratings")
        st.write(st.session_state.df_feedback)
        download_button()
        st.divider()
        
    #if(len(st.session_state.df_feedback_unknown) > 0):
    #    st.write("Without Category")
    #    st.write(st.session_state.df_feedback_unknown)
    #    st.divider()


    if(len(st.session_state.df_feedback) > 0):
        # Create a stacked bar chart

    #col1, col2 = st.columns(2)

    #with col1:
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

        
        #col1 and col3 is not used
        col1, col2, col3 = st.columns([1,3,1])

        with col2:
            
            result = ' '.join([word for sublist in st.session_state.df_feedback["keywords"] for word in sublist])
            
            if(len(result)) > 0:

                st.markdown("""
                    <style>
                    .title {
                        text-align: center;
                        font-size: 20px;
                        font-weight: bold;
                    }
                    </style>
                    <div class="title">WordCloud from Keywords</div>
                    """,
                    unsafe_allow_html=True
                )

                # Create and generate a word cloud image:
                book_mask = np.array(Image.open('image/blank.jpg'))

                wordcloud = WordCloud(width=8, height=5, background_color='lightblue',mask=book_mask,
                                    contour_color='black', contour_width=3).generate(result)
                
                # Display the word cloud using matplotlib

                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')  # Hide the axes

                # Show the plot in Streamlit
                st.pyplot(plt)

        #with col2:
        df = st.session_state.df_feedback[st.session_state.df_feedback['category'] != 'Unknown'][['sentiment', 'rating']]
        
        # Set up color mapping
        color_map = {
            'positive': 'green',
            'negative': 'red',
            'neutral': 'gray',
            'mixed':'orange'
        }

        # Add a color column to the DataFrame based on sentiment
        df['color'] = df['sentiment'].map(color_map)

        # Create a scatter plot with individual ratings
        plt.figure(figsize=(10, 6))

        plt.gcf().set_facecolor('whitesmoke')  # Change the figure background color
        plt.gca().set_facecolor('lightblue')  # Change the axes background color

        plt.scatter(df['rating'], range(len(df)), 
                    c=df['color'].tolist(),  # Convert color Series to a list
                    s=100,  # Set a fixed size for clarity
                    alpha=0.6)  # Optional: make markers semi-transparent

        plt.axvline(0, color='black', lw=0.8)  # Add a vertical line at x=0
        plt.xlim(-100, 100)  # Set x limits

        plt.title('Sentiment Ratings')
        plt.xlabel('Rating')
        plt.ylabel('Feedback')
        #plt.grid(True)

        # Create a circular legend below the plot
        handles = [mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=sentiment) 
           for sentiment, color in color_map.items()]
        plt.legend(handles=handles, title='Sentiment', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

        # Show the plot in Streamlit
        st.pyplot(plt)