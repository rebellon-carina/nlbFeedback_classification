import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="ABout"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("We are a dynamic team dedicated to revolutionizing the way libraries categorize and deliver information. With the power of artificial intelligence and a passion for enhancing user experience, we’ve created a platform that transforms feedback into intuitive categories")

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

st.divider()
st.markdown("### Cloak API Anonymizer")
st.markdown("""
            |Person Name | NRIC | Bank Account Number | Address | Phone Number | Email Address|
            |----------- |----------- |----------- |----------- |----------- |-----------|
            |Replaced by <√> |Replaced by <SG_NRIC_FIN> |Replaced by <<SG_BANK_ACCOUNT_NUMBER>> |Replaced by <G_ADDRESS> |Masked First 4 chars with * |encrypt|
             
          
            
            """)
st.divider()
st.markdown("### List of Categories and Sub-categories")

st.markdown(f"""
                |:blue[*Feedback Category*]|Collection-e|Collection-Print|Customer Service|Environment|Policies & Procedures|Programmes|Services & Facilities|
                |-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|
                |:blue[Feedback Sub-category]|Availability|Availability|Others|Cleanliness|Cashless payment|Event Publicity - GoLibrary|Book Borrowing station|
                ||Others|Others|Staff|Furniture (condition)|Circulation|Event Publicity - others|Book drop|
                ||Variety|Review of titles|Vendor|Noise|Claim return|Exhibition|Catalogue|
                |||Shelving||Others|Donation|Loan promotion|DIYRead Services|
                |||Vandalism||Seating Availability|Fine mailers|Others|Ekiosk|
                |||Variety||Signage |Library Etiquette-others|Presentation|Rresources|
                |||||Toilets|Library Etiquette - Studying|Registration|Facilities Booking Services|
                |||||Library fines|Speaker|Microfilm Services |
                ||||||Membership-Basic|Variety|Mobile App|
                ||||||Membership-Premium Plus|Venue|Multimedia Stations|
                ||||||Opening Hours||myLibrary ID|
                ||||||Others||NAS Website|
                ||||||Researcher Pass||NLB Website|
                ||||||Reservation fee & policy||Online renewal|
                ||||||||Online reservation|
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
            """)


st.write('*A POC project by CHR and GJ of NLB*')
