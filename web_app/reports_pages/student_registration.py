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


# Page title and introduction
st.title("Student Registration")

# Introducing the Student's Registration page

st.markdown("""

#### Welcome to the Student Registration Report Report.
            
This section provides a comprehensive overview of student enrollment 
            data across different academic sessions and levels.

Here, you can explore:
- **Number of Students by Session:** Track the number of students 
enrolled in each academic session to understand enrollment trends and shifts over time.

- **Number of Students by Level:** Gain insights into the distribution 
of students across various academic levels, helping to identify trends and needs at each level.

            
The slicers can be used to filter data by session, and academic level 
to get a detailed and customized view of the performance metrics.

This dynamic feature allows the viewing of specific areas of interest.
""")


# Visualizations
st.write("# Data Visualizations")
st.write("This is where the visualizations and detailed analysis will be displayed.")




