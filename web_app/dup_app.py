import streamlit as st
from data_loader import load_data

# st.set_page_config(page_title="Multipage Streamlit App", layout="wide")

# Load the data once and use it across all reports_reports_pages
data = load_data()

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", [
    "Home", 
    "Demographics", 
    "Enrollment Trend", 
    "Students Registration", 
    "Grade Distribution", 
    "Course Performance", 
    "Academic Performance Over Time", 
    "Overall Performance", 
    "Comparative Analysis"
])

if page == "Home":
    import reports_pages.home as home
    home.app(data)
elif page == "Demographics":
    import reports_pages.demographics as demographics
    demographics.app(data)
elif page == "Enrollment Trend":
    import reports_pages.enrollment_trend as enrollment_trend
    enrollment_trend.app(data)
elif page == "Students Registration":
    import reports_pages.student_registration as students_registration
    students_registration.app(data)
elif page == "Grade Distribution":
    import reports_pages.grade_distribution as grade_distribution
    grade_distribution.app(data)
elif page == "Course Performance":
    import reports_pages.course_performance as course_performance
    course_performance.app(data)
elif page == "Academic Performance Over Time":
    import reports_pages.academic_performance_over_time as academic_performance_over_time
    academic_performance_over_time.app(data)
elif page == "Overall Performance":
    import reports_pages.overall_performance as overall_performance
    overall_performance.app(data)
elif page == "Comparative Analysis":
    import reports_pages.comparative_analysis as comparative_analysis
    comparative_analysis.app(data)
