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


#-------------------------- Total Number of Registered Students  ----------------------------

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

def plot_students_by_state(Biodata):
    # Replace missing or unknown values with 'Unknown'
    Biodata['State_of_Origin'] = Biodata['State_of_Origin'].replace('-', 'Unknown')

    # Grouping by State_of_Origin and counting the number of students per state
    state_counts = Biodata['State_of_Origin'].value_counts().reset_index()
    state_counts.columns = ['State_of_Origin', 'Number_of_Students']

    # Sort the dataframe by Number_of_Students in descending order
    state_counts = state_counts.sort_values(by='Number_of_Students', ascending=True)

    # Create a slider for adjusting the height of the plot
    plot_height = st.slider('Select plot height For clearer view',
                            min_value=400, max_value=1000, value=600, step=50)

    # Create a horizontal bar chart using Plotly
    fig = px.bar(state_counts, 
                 x='Number_of_Students', 
                 y='State_of_Origin', 
                 orientation='h',
                 title='Number of Students by State of Origin',
                 color_discrete_sequence=['#DE6A73'],  # Same color for all bars
                 text='Number_of_Students',
                 labels={'Number_of_Students': 'Number of Students', 'State_of_Origin': 'State of Origin'})

    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Number of Students',
        yaxis_title='State of Origin',
        xaxis=dict(showgrid=True),  # Show grid lines
        height=plot_height,  # Adjustable height based on the slider
        width=1000,  # Adjustable width
        showlegend=False  # Remove the legend
    )

    # Add data labels to the bars
    fig.update_traces(texttemplate='%{text}', textposition='outside')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

# Example usage in Streamlit
st.write(
    """
    <div>
        <h4>Number of Students by State of Origin</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# Call the function with the Biodata DataFrame
plot_students_by_state(Biodata)





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


# Assuming Biodata is already loaded as a DataFrame
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
        textfont=dict(size=12, color="white"),  # Adjust font size for text inside arcs
        hoverinfo='label+value',
        showlegend=True  # Show legend for interactivity
    )])
    
    fig.update_layout(
        title_text=title,
        title_font_size=14,  # Increase font size for the title
        title_font_color="white",  # Change title font color
        annotations=[dict(
            text=annotation, 
            x=0.5, y=0.5, 
            font_size=16, 
            showarrow=False, 
            font_color="white"  # Change this color to improve visibility
        )],
        #paper_bgcolor="black",  # Background color of the entire figure
        plot_bgcolor="black",  # Background color of the plotting area
        margin=dict(t=60, b=40, l=40, r=40),  # Adjust the margins as needed
        height=300,  # Height of the box
        width=300,   # Width of the box
        font_color="white"  # Font color for text outside the chart
    )
    
    return fig

# Create the doughnut charts
gender_fig = create_doughnut_chart(gender_counts.index, gender_counts.values, "Number of Students by Gender", "Gender")
marital_status_fig = create_doughnut_chart(marital_status_counts.index, marital_status_counts.values, "Number of Students by Marital Status", "Marital Status")

# Create two columns and place the doughnut charts side by side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(gender_fig, use_container_width=True)

with col2:
    st.plotly_chart(marital_status_fig, use_container_width=True)



st.markdown("<br><br><br><br>", unsafe_allow_html=True)


# ----------------------- Number of Students by Nationality and Religion ------------------------

# Function to plot vertical bar chart using Plotly
def plot_vertical_bar_chart(dataframe, column, color):
    # Calculate value counts for the specified column
    counts = dataframe[column].value_counts().reset_index()
    counts.columns = [column, 'Number of Students']

    # Create the bar chart using Plotly
    fig = px.bar(counts, x=column, y='Number of Students', text='Number of Students',
                 color_discrete_sequence=[color])

    # Update layout for a non-white background and adjust text colors
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        font=dict(color='white'),  # White text color
        title={
            'text': f'\nNumber of Students by {column}\n',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        title_font_size=16,
        xaxis_title=column,
        yaxis_title='Number of Students',
        yaxis=dict(showgrid=False, zeroline=False),
        xaxis=dict(showgrid=False, zeroline=False)
    )

    # Add data labels on top of the bars
    fig.update_traces(textposition='outside', textfont=dict(size=12, color='white'))

    return fig

# Create two columns for side-by-side layout
col1, col2 = st.columns(2)

# Plot for Nationality
with col1:
    fig1 = plot_vertical_bar_chart(Biodata, 'Nationality', '#DE6A73')
    st.plotly_chart(fig1)

# Plot for Religion
with col2:
    fig2 = plot_vertical_bar_chart(Biodata, 'Religion', '#DE6A73')
    st.plotly_chart(fig2)
