import pandas as pd
import os
import streamlit as st

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, 'Student_Data.xlsx')

#file_path = "Student_Data.xlsx"

@st.cache_data
def load_data():
    # Load the Excel file
    
    # Load the individual sheets into dataframes
    Academic_Performance = pd.read_excel(file_path, sheet_name='Academic_Performance')
    Biodata = pd.read_excel(file_path, sheet_name='Biodata')
    First_and_Last_Result = pd.read_excel(file_path, sheet_name='First_and_Last_Result')
    Registration = pd.read_excel(file_path, sheet_name='Registration')
    Result_Sheet = pd.read_excel(file_path, sheet_name='Result_sheet')
    
    return {
        "Academic_Performance": Academic_Performance,
        "Biodata": Biodata,
        "First_and_Last_Result": First_and_Last_Result,
        "Registration": Registration,
        "Result_Sheet": Result_Sheet
    }
