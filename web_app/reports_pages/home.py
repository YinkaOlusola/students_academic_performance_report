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


# Writing the title of the home page
st.title("Student Academic Performance Dashboard")
#st.write(data['Biodata'].head())

# Welcome note
st.markdown("""
Welcome to the Student Academic Performance Dashboard. \nThis dashboard provides \
            insights into the academic performance of students of Computer Science\
            over 20 sessions.
            \nUse the navigation menu to explore different sections of the dashboard.
""")

st.markdown("\n")

# Instructions on Navigation
st.markdown("""
**Navigation Guide:**

- **Demographics**: Explore detailed demographic insights, including age, \
            gender, and geographic distribution of the student population. 
            This page provides a comprehensive overview of the demographics 
            that shape our academic environment, helping to understand trends 
            and patterns within the student body..

- **Enrollment Trend**: Explore the historical trends in student enrollment 
            with this page. Visualize patterns and changes in enrollment 
            numbers over time, understand peak enrollment periods, and analyze 
            trends across different academic years or terms.

- **Student Registration**: Explore the Student Registration page to view and 
            manage detailed information about student enrollments. This section 
            provides insights into the registration process, including the number 
            of new registrations, and registration trends over 
            time. Whether you are tracking student onboarding or analyzing 
            registration patterns, this page offers a comprehensive view of student 
            registration activities.

- **Grade Distribution**: The Grade Distribution page provides a comprehensive 
            overview of the distribution of grades across various courses. 
            It includes visualizations that highlight how grades 
            are spread among different ranges and categories. This page helps in 
            understanding grading trends and identifying patterns in student performance.

- **Course Performance**: Explores analyses of student performance across 
            various courses. This page provides insights into how students are 
            performing in individual courses, highlighting trends, identifying 
            high and low-performing courses, and allowing for comparisons between 
            different course sections and instructors. Use this tool to gain a 
            deeper understanding of academic outcomes and improve course offerings.

- **Academic Performance Over Time**: Explores trends in academic performance across 
            different semesters or years. This page provides insights into how 
            student performance has evolved over time, highlighting key patterns and 
            variations that can inform academic planning and decision-making.

- **Overall Performance**: This page provides a detailed overview of student graduation 
            outcomes, categorized by the classification of their final CGPA. It 
            highlights the distribution of graduates across different honors 
            classifications, such as First Class, Second Class, and others. Use this 
            page to understand how students are performing at the culmination of their 
            studies and to assess the overall academic achievements within the institution. 

- **Comparative Analysis**: Delve into detailed comparisons of student performance by 
            session, including CGPA classification and academic level. This page also 
            features analyses of the average First CGPA, average Final CGPA, and the 
            relationship between First and Final CGPA, providing valuable insights 
            into academic progression.
""")

st.empty()

st.write("\n\n")

# User Instructions and Tips
st.markdown("""
**Tips:**
- Use the filters on the left sidebar to narrow down your analysis.

- For detailed reports, navigate to the specific sections using the menu.
""")


# Foot Note
#st.markdown("**App Version**: 1.0.0 | **Last Updated**: August 2024")




