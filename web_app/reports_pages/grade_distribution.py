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


st.title("Grade Distribution Report")

st.markdown("""

#### Welcome to the Grade Distribution Report.
 
Here, an insightful analysis of how grades are distributed across different courses 
is presented. This page visualizes the number of students who have achieved 
various grades in each course, allowing the assessment of the overall performance and 
grading trends within the academic programs.

By exploring this data, one can identify patterns in student performance, evaluate 
the effectiveness of grading standards, and make informed decisions to support 
academic development.
            
Use the interactive charts and graphs below to gain a deeper 
understanding of the distribution of grades and uncover any notable trends.
""")


# Visualization
st.write("# Data Visualizations")
st.write("This is where the visualizations and detailed analysis will be displayed.")




