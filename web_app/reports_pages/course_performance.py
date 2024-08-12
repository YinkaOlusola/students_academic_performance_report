import streamlit as st
from data_loader import load_data

# Loading the data
data = load_data()

# Passing the Data into Variables
Academic_Performance = data["Academic_Performance"]
Biodata = data["Biodata"]
First_and_Last_Result = data["First_and_Last_Result"]
Registration = data["Registration"]
Result_Sheet = data["Result_Sheet"]


# Title for the page
st.title("Course Performance")

st.write("""

#### Welcome to the Course Performance page!

This section provides a comprehensive overview of academic performance 
across various courses. Here, the following key metrics can be explored:

- **Average Scores**: View the average scores obtained in each course, 
         providing insight into overall performance trends.

- **Minimum Scores**: Identify the lowest scores recorded, helping to 
         understand areas needing improvement.

- **Maximum Scores**: Discover the highest scores achieved, celebrating 
         exceptional academic achievements.

The slicers can be used to filter data by session, course, and academic level 
to get a detailed and customized view of the performance metrics. This dynamic 
feature allows you to pinpoint specific areas of interest and assess 
         performance comprehensively.
""")



# Visualizations
st.write("# Data Visualizations")
st.write("This is where the visualizations and detailed analysis will be displayed.")



