import numpy as np
import pandas as pd
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

# Display the title and introductory text
st.title("Academic Performance Over Time")

st.markdown("""

#### Welcome to the Academic Performance Over Time report.

This page provides an in-depth analysis of student academic performance 
trends across different sessions. The visualizations and metrics 
here are designed to help you understand the following aspects:

1. **Average GPA and CGPA by Session**: Track the average GPA and CGPA 
of students for each academic session to observe performance trends over time.

2. **Trend of Number of Students by CGPA Classification**: Analyze how the 
distribution of students across different CGPA classifications changes from 
one session to another.

3. **Course Performance**: Evaluate the performance of students in various 
courses and observe trends in their academic achievements.

4. **Number of Students per Session by CGPA and Classification**: Get 
insights into the number of students in each session categorized by 
their CGPA and classification.

Additionally, you can use the interactive slicers to filter the data based 
on CGPA classification, semester, and academic level. This flexibility 
allows you to focus on specific segments of the data and gain more targeted insights.

Explore the data to uncover trends, identify areas for improvement, and celebrate achievements. The visualizations and filters will assist you in making data-driven decisions to enhance academic performance.
""")


# Data Visualization
st.write("# Visualization")







st.write(data["Academic_Performance"].head())


# Sidebar
st.sidebar.title('Session')
# Include 'None' for select all
options = ['Select All'] + list(data["Academic_Performance"]["Session"].unique())
selected_categories = st.sidebar.multiselect('Select Session:', options)

# Handling 'None' selection to select all
if 'Select All' in selected_categories:
    selected_categories = data["Academic_Performance"]["Session"].unique()


# Filtered DataFrame
filtered_df = data["Academic_Performance"][data["Academic_Performance"]["Session"].isin(selected_categories)]

st.write("\n")

# Display filtered data
st.write('Filtered DataFrame:')
st.write("\n")
st.write(filtered_df)






























def app(data):
    st.title("Academic Performance")
    st.write("Welcome to the Academic Performance Page")

    st.write(data['Biodata'])
