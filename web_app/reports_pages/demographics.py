import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

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


st.title("Students' Demographics Report")

st.markdown("""

#### Welcome to the Students' Demographics Page.

This Page provides a comprehensive overview of the student population, 
offering valuable insights into various demographic attributes. Here, you 
will find detailed statistics on key aspects of the student body, including:

1. **Number of Students by State of Origin**: Discover the geographic diversity of 
            student population, with data on the number of students from each state.

2. **Total Number of Registered Students**: View the overall number of students who 
            have been enrolled.

3. **Total Number of Students with Biodata**: See how many students have 
            complete biodata information.

4. **Total Number of Graduated Students**: Track the number of students who have 
            successfully completed their studies.

5. **Number of Students by Gender (based on Biodata)**: Explore the gender 
            distribution of students based on the available biodata.

6. **Number of Students by Nationality**: Gain insights into the international 
            composition of our student community, with data on the number of 
            students from different countries.

7. **Number of Students by Marital Status**: Analyze the marital status of 
            students to better understand their demographics.

8. **Number of Students by Religion**: Understand the religious diversity within 
            the student population.

This demographic data helps us better understand the composition of the student body, 
ensuring that we can tailor our programs and services to meet the needs of our diverse 
community. Explore the dashboard to gain further insights into these key demographic areas.
""")

st.markdown("<br><br><br><br>", unsafe_allow_html=True)


# Visualizations
st.write("# Data Visualizations")


st.markdown("<br><br><br>", unsafe_allow_html=True)


######### Total Number of Registered Students ############

# Count the number of distinct Matric_Number
distinct_students = Registration['Matric_Number'].nunique()
student_with_biodata = Biodata["Matric_Number"].nunique()
# Number of Graduated Students
graduated_students = First_and_Last_Result[(First_and_Last_Result['Last_GPA'] > 1) & 
                                           (First_and_Last_Result['Last_CGPA'] > 1)].shape[0]

# Layout with three columns
col1, col2, col3 = st.columns(3)

# Number of Registered Students
with col1:
    st.write(
        f"""
        <div style="background-color: #e9ecef; padding: 5px; border-radius: 5px; text-align: center;">
            <h4 style="margin: 0; color: #007bff">Total Number of Registered Students</h4>
            <h1 style="margin: 0; color: #007bff">{distinct_students}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Total Number of Students with Biodata
with col2:
    st.write(
        f"""
        <div style="background-color: #f8f9fa; padding: 5px; border-radius: 5px; text-align: center;">
            <h4 style="margin: 0; color: #007bff">Total Number of Students with Biodata</h4>
            <h1 style="margin: 0; color: #007bff;">{student_with_biodata}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Total Number of Graduated Students
with col3:
    st.write(
        f"""
        <div style="background-color: #e9ecef; padding: 5px; border-radius: 5px; text-align: center;">
            <h4 style="margin: 0; color: #007bff">Total Number of Graduated Students</h4>
            <h1 style="margin: 0; color: #007bff">{graduated_students}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br><br><br><br>", unsafe_allow_html=True)


#-------------------------- Number of Students by State of Origin -----------------------------

st.write(
    f"""
    <div>
        <h4>Number of Students by State of Origin</h4>
    </div>
    """,
    unsafe_allow_html=True
    )

# Replace missing or unknown values with 'Unknown'
Biodata['State_of_Origin'] = Biodata['State_of_Origin'].replace('-', 'Unknown')

# Grouping by State_of_Origin and counting the number of students per state
state_counts = Biodata['State_of_Origin'].value_counts().sort_values(ascending=False)

# Create a horizontal bar chart
plt.figure(figsize=(12, 10))
bars = sns.barplot(x=state_counts.values, y=state_counts.index, color="#DE6A73")

# Add labels to the bars
for index, value in enumerate(state_counts):
    plt.text(value + 1, index, str(value), va='center', ha='left', fontsize=8, color='black')

plt.title('Number of Students by State of Origin')
plt.xlabel('Number of Students')
plt.ylabel('State of Origin')

# Display the plot in Streamlit
st.pyplot(plt)


st.markdown("<br><br><br><br>", unsafe_allow_html=True)


#------------------------------ Number of Students by Gender and Marital Status -----------------------

st.write(
    f"""
    <div>
        <h4>Number of Students by Gender and Marital Status</h4>
    </div>
    """,
    unsafe_allow_html=True
    )


# Calculate the counts of each gender and marital status
gender_counts = Biodata['Sex'].value_counts()
marital_status_counts = Biodata['Marital_Status'].value_counts()

# Function to create a doughnut chart
def create_doughnut_chart(labels, values, title, annotation):
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=0.5,  # Creates the hole for the doughnut chart
        marker=dict(colors=['#DE6A73', '#E8D166']),
        textinfo='label+percent',  # Show label and percent in the chart
        textfont=dict(size=12, color="black"),  # Adjust font size for text inside arcs
        hoverinfo='label+value',
        showlegend=False
    )])

    
    fig.update_layout(
        title_text=title,
        title_font_size=14,  # Increase font size for the title
        title_font_color="black",  # Change title font color
        annotations=[dict(
            text=annotation, 
            x=0.5, y=0.5, 
            font_size=20, 
            showarrow=False, 
            font_color="black"  # Change this color to improve visibility
        )],
        paper_bgcolor="white",  # Background color of the entire figure
        plot_bgcolor="white",  # Background color of the plotting area
        margin=dict(t=60, b=40, l=40, r=40),  # Adjust the margins as needed
        height=400,  # Height of the box
        width=400,   # Width of the box
    )
    
    return fig

# Create the doughnut charts
gender_fig = create_doughnut_chart(gender_counts.index, gender_counts.values, "Number of Students by Gender", "Gender")
marital_status_fig = create_doughnut_chart(marital_status_counts.index, marital_status_counts.values, "Number of Students by Marital Status", "Marital Status")

# Create two columns and place the doughnut charts side by side
col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(gender_fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:

    st.plotly_chart(marital_status_fig)
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<br><br><br><br>", unsafe_allow_html=True)


# ----------------------------- Number of Students by Nationality ---------------------------------

st.write(
    f"""
    <div>
        <h4>Number of Students by Nationality and Religion</h4>
    </div>
    """,
    unsafe_allow_html=True
    )


def plot_vertical_bar_chart(dataframe, column, color):
    plt.figure(figsize=(6, 4))
    counts = dataframe[column].value_counts()
    sns.barplot(x=counts.index, y=counts.values, palette=[color])
    plt.xlabel(column)
    plt.ylabel('Number of Students')
    plt.title(f'Students by {column}')
    for p in plt.gca().patches:
        plt.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2, p.get_height() + 0.2),
                     va='bottom', ha='center', fontsize=10, color='black')


# Create two columns for side-by-side layout
col1, col2 = st.columns(2)

# Plot for Nationality
with col1:

    plot_vertical_bar_chart(Biodata, 'Nationality', '#DE6A73')
    st.pyplot(plt.gcf())
    plt.close()  # Close the plot to avoid overlap

# Plot for Religion
with col2:

    plot_vertical_bar_chart(Biodata, 'Religion', '#DE6A73')
    st.pyplot(plt.gcf())
    plt.close()  # Close the plot to avoid overlap



 


























































































def app(data):
    st.title("Student Demographics")
    st.write("Welcome to the Students Demographics Report")

    st.write(data['Biodata'])
