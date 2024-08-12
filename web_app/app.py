# Importing the Streamlit app
import streamlit as st
from data_loader import load_data


# Load the data once and use it across all reports_reports_pages
data = load_data()


# Define the pages for the Streamlit app

# Home page configuration
# This page will serve as the home page with a file located at "reports_pages/home.py".
home = st.Page(
    "reports_pages/home.py",  # Path to the home page script
    title="Home",             # Title of the page
    icon="",                  # Icon for the page (empty for no icon)
    default=True              # Set this page as the default one
)

# Demographics page configuration
# This page displays demographic information with its content in "reports_pages/demographics.py".
demographics = st.Page(
    page="reports_pages/demographics.py",  # Path to the demographics page script
    title="Demographics",                  # Title of the page
    url_path="demographics.py"             # URL path for the page
)

# Enrollment Trend page configuration
# This page shows trends in enrollment, and its content 
# is sourced from "reports_pages/enrollment_trend.py".
enrollment_trend = st.Page(
    page="reports_pages/enrollment_trend.py",  # Path to the enrollment trend page script
    title="Enrollment Trend",                 # Title of the page
    icon=""                                   # Icon for the page (empty for no icon)
)

# Students Registration page configuration
# This page covers student registration details, with 
# content from "reports_pages/student_registration.py".
students_registration = st.Page(
    page="reports_pages/student_registration.py",  # Path to the students registration page script
    title="Students Registration",                # Title of the page
    icon=""                                       # Icon for the page (empty for no icon)
)

# Grade Distribution page configuration
# This page visualizes the distribution of grades,
# sourced from "reports_pages/grade_distribution.py".
grade_distribution = st.Page(
    page="reports_pages/grade_distribution.py",  # Path to the grade distribution page script
    title="Grade Distribution",                  # Title of the page
    icon=""                                     # Icon for the page (empty for no icon)
)

# Course Performance page configuration
# This page evaluates the performance of different courses, 
# with content from "reports_pages/course_performance.py".
course_performance = st.Page(
    page="reports_pages/course_performance.py",  # Path to the course performance page script
    title="Course Performance",                  # Title of the page
    icon=""                                      # Icon for the page (empty for no icon)
)

# Academic Performance Over Time page configuration
# This page tracks academic performance over time, sourced
# from "reports_pages/academic_performance_over_time.py".
academic_performance_over_time = st.Page(
    page="reports_pages/academic_performance_over_time.py",  # Path to the academic performance over time page script
    title="Academic Performance Over Time",                 # Title of the page
    icon=""                                                # Icon for the page (empty for no icon)
)

# Overall Performance page configuration
# This page provides an overview of overall performance,
# with content from "reports_pages/overall_performance.py".
overall_performance = st.Page(
    page="reports_pages/overall_performance.py",  # Path to the overall performance page script
    title="Overall Performance",                  # Title of the page
    icon=""                                       # Icon for the page (empty for no icon)
)

# Comparative Analysis page configuration
# This page offers comparative analysis, and its content
# is located in "reports_pages/comparative_analysis.py".
comparative_analysis = st.Page(
    page="reports_pages/comparative_analysis.py",  # Path to the comparative analysis page script
    title="Comparative Analysis",                  # Title of the page
    icon=""                                        # Icon for the page (empty for no icon)
)

# Set up the navigation menu for the app
# Define a navigation menu titled "Reports" with links to all the defined pages.
pg = st.navigation({
    "Reports": [home, demographics, enrollment_trend,
                students_registration, grade_distribution,
                course_performance, academic_performance_over_time,
                overall_performance, comparative_analysis]
})

# Run the Streamlit app
# Run the Streamlit app with the navigation configuration
pg.run()

