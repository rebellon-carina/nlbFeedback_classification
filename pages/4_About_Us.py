import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="About"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("We are a dynamic team dedicated to transforming the way libraries service our customers. With the power of artificial intelligence and a passion for enhancing user experience, we’ve created a platform that classifies feedback into intuitive categories.")

with st.expander("How to use this App"):
    st.markdown("""
                1. In the main app, locate the 'Entry Feedback Form' area.
                    -   You can submit feedback in two ways:
                        -   a. Enter one feedback item at a time.
                        -   b. Copy and paste a list of feedback from Excel. Ensure each item is separated by a new line.
                    If any feedback item contains a new line, enclose it in double quotes to ensure it is treated as a single entry.
                2. Click the 'Submit' button. This may take a while depeds on how many feedback is entered. If the Cloak API is enabled, it will masked the sensitive information first before processing.
                    - *Check details below for personal information that will be anonymized*
                3. The app will generate the Category and Sub-category based on the feedback(s). It can assign more than one Categories or Sub-categories. Below is the summary of all Categories and Sub-categories
                """)

# st.divider()
with st.expander("Problem Statement"):
    st.markdown("""
                NLB receives free-text feedback from our customers through two main sources:
                1. Responses to open-ended questions asked in our annual Customer Satisfaction Survey.
                2. Emails sent to our customer service enquiry mailbox manned by the Service Excellence Office. 
                The two sources are manually coded into categories to be sent to relevant divisions for follow-up.
                
                Both sources are currently using independent codeframes with different pre-defined actegories,\
                 making it challenging to consolidate free-text feedback across the two sources to spot common trends.\
                In order to analyse and understand this rich textual data, each source should be tagged using a common methodology,\
                saving time and costs. 
                """)

with st.expander("List of Categories and Sub-categories"):
    st.markdown("##### Table of Categories and Sub-categories that are provided to LLM for reference.")

    st.markdown(f'''
                    |:blue[*Category*]|Collection-e|Collection-Print|Customer Service|Environment|Policies & Procedures|Programmes|Services & Facilities|
                    |-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|
                    |:blue[Sub-category]|Availability|Availability|Others|Cleanliness|Cashless payment|Event Publicity - GoLibrary|Book Borrowing station|
                    ||Others|Others|Staff|Furniture (condition)|Circulation|Event Publicity - others|Book drop|
                    ||Variety|Review of titles|Vendor|Noise|Claim return|Exhibition|Catalogue|
                    |||Shelving||Others|Donation|Loan promotion|DIYRead Services|
                    |||Vandalism||Seating Availability|Fine mailers|Others|Ekiosk|
                    |||Variety||Signage |Library Etiquette-others|Presentation|Rresources|
                    |||||Toilets|Library Etiquette - Studying|Registration|Facilities Booking Services|
                    |||||Library fines|Speaker|Microfilm Services|Mobile App|
                    ||||||Membership-Basic|Variety|Multimedia Stations|
                    ||||||Membership-Premium Plus|Venue|myLibrary ID|
                    ||||||Opening Hours||NAS Website|
                    ||||||Others||NLB Website|
                    ||||||Researcher Pass||Online renewal|
                    ||||||Reservation fee & policy||Online reservation|
                    ||||||||Others|
                    ||||||||Photocopying services|
                    ||||||||Powerpoint outlets|
                    ||||||||READ@Community services|
                    ||||||||Reference services|
                    ||||||||Reminder services|
                    ||||||||Reservation services - Others|
                    ||||||||Reservation services - Reservation Lockers|
                    ||||||||Scanning services|
                    ||||||||Wireless Internet services|
                
                ''',
            unsafe_allow_html=True)

# st.divider()
with st.expander("Cloak API Integration"):
    st.markdown("###### When enabled, this app automatically sends any feedback inputted to Cloak for anonymization before\
                sending them to the LLM.")
    st.markdown("""
                |Person Name | NRIC | Bank Account Number | Address | Phone Number | Email Address|
                |----------- |----------- |----------- |----------- |----------- |-----------|
                |Replaced by <PERSON NAME> |Replaced by <SG_NRIC_FIN> |Replaced by <SG_BANK_ACCOUNT_NUMBER> |Replaced by <G_ADDRESS> |Masked First 4 chars with * |encrypt|
                
            
                
                """)

    st.write('*A POC project by CHR and GJ of NLB*')
