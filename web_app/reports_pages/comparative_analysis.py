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


st.title("Overall Performance Overview")

st.write("""
#### Welcome to the Overall Performance Report page.
 
This section provides an insightful analysis of the academic achievements 
of students across various sessions. The primary focus here is on the 
number of graduating students categorized by their final 
Cumulative Grade Point Average (CGPA) classifications.

In this report, the following can be explored:
         
- **Number of Graduating Students**: View the count of students 
who have graduated based on different CGPA classifications.

- **CGPA Classification**: Understand the distribution of students across 
various performance brackets, helping to gauge the overall academic 
performance of the student body.

- **Session Filter**: Use the slicer to filter the data by specific 
academic sessions to view performance trends over time.

Interact with the report to gain a comprehensive 
understanding of academic performance and track the 
progress of graduating students by their final CGPA.
         
""")


