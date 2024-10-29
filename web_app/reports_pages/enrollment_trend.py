import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
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


st.title("Enrollment Trend Analysis")

st.markdown("""

#### Welcome to the Enrollment Trend Section. 
         
This Section provides an in-depth look at how student enrollment has evolved over 
time, offering key insights into the patterns and changes in student demographics.

The report is designed to give a comprehensive view of the following trends:

1. **Trend of Number of Students by Session:** Explore how the total number of 
         students has varied across different academic sessions, highlighting 
         periods of growth or decline.

2. **Trend of Admitted Students by Year of Admission:** Delve into the yearly 
         admission trends, identifying the influx of new students over the years 
         and understanding the factors that may influence these patterns.

3. **Number of Students Admitted by Year and Gender:** Analyze the gender 
         distribution among admitted students year by year, offering insights 
         into gender diversity and shifts over time.

These visualizations will help one to better understand the dynamics of student 
         enrollment and support data-driven decision-making for academic 
         planning and resource allocation. 

Explore the data and uncover the stories behind the numbers!
""")


st.markdown("<br><br><br>", unsafe_allow_html=True)


# Visualizations
st.write("# Data Visualizations")

st.markdown("<br>", unsafe_allow_html=True)

#------------------------------ Total Number of Students by Session ------------------------------

# Correcting the wrong entries in the Session column
Registration['Session'] = Registration['Session'].replace({
    '90-92': '1990-1991',
    '97/98': '1997-1998'
})

# Grouping the data by 'Session' and counting the number of unique 'Matric_Number'
students_by_session = Registration.groupby('Session')['Matric_Number'].nunique().reset_index()

# Creating the line chart using Plotly Express
fig = px.line(students_by_session, 
              x='Session', 
              y='Matric_Number', 
              title='Trend of Number of Students by Session',
              labels={'Matric_Number': 'Number of Students', 'Session': 'Session'})

# Customizing the line color
fig.update_traces(line=dict(color='#DE6A73'))

# Displaying the chart in Streamlit
st.plotly_chart(fig)



st.markdown("<br><br><br>", unsafe_allow_html=True)


#------------------------- Trend of Admitted Students by Year of Admission --------------------------


# Grouping the data by 'Session' and counting the number of unique 'Matric_Number'
students_by_YOA = Biodata.groupby('YOA')['Matric_Number'].nunique().reset_index()

# Creating the line chart using Plotly Express
fig = px.line(students_by_YOA, 
              x='YOA', 
              y='Matric_Number', 
              title='Trend of Admitted Students by Year of Admission',
              labels={'Matric_Number': 'Number of Admitted Students', 'YOA': 'Year of Admission'})

# Customizing the line color
fig.update_traces(line=dict(color='#DE6A73'))

# Displaying the chart in Streamlit
st.plotly_chart(fig)


st.markdown("<br><br><br>", unsafe_allow_html=True)




#------------------- Number of Admitted Students by Year of Admission and Gender --------------------

# Assuming Biodata is already loaded as a DataFrame
# Group by YOA and Sex, and count the number of students
biodata_grouped = Biodata.groupby(['YOA', 'Sex']).size().reset_index(name='count')

# Sort by YOA in descending order based on the total number of students admitted
biodata_grouped['YOA'] = pd.Categorical(
    biodata_grouped['YOA'], 
    categories=biodata_grouped.groupby('YOA')['count'].sum().sort_values(ascending=False).index,
    ordered=True
)

plot_height = st.slider('Adjust plot height for Visibility', min_value=100, max_value=800, value=400)

# Create the base chart with stacked bars
bars = alt.Chart(biodata_grouped).mark_bar().encode(
    x=alt.X('count:Q', title='Number of Students'),
    y=alt.Y('YOA:O', sort='-x', title='Year of Admission (YOA)'),
    color=alt.Color('Sex:N', scale=alt.Scale(range=['#E1C233', '#DE6A73']), title='Gender'),
    order=alt.Order('Sex:N', sort='ascending'),
    tooltip=['YOA', 'Sex', 'count']
)

# Create text labels for the bars with improved visibility
text = alt.Chart(biodata_grouped).mark_text(
    dx=-8,  # Slight adjustment to avoid overlapping with bar edges
    color='black'  # Set the label color to black for better visibility
).encode(
    x=alt.X('count:Q', stack='zero'),  # Use stack='zero' to align text with stacked bars
    y=alt.Y('YOA:O', sort='-x'),
    text=alt.Text('count:Q', format='.0f')  # Display the count as text
)

# Combine the bar chart and text labels
chart = (bars + text).properties(
    title='Number of Students Admitted by Year and Gender',
    width=600,
    height=plot_height
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16
).configure_legend(
    titleFontSize=12,
    labelFontSize=10
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
