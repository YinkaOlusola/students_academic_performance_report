import numpy as np
import pandas as pd
import streamlit as st
from data_loader import load_data
import plotly.express as px
import plotly.graph_objects as go

# Loading the data
data = load_data()

# Passing the Data into Variables
Academic_Performance = data["Academic_Performance"]
Biodata = data["Biodata"]
First_and_Last_Result = data["First_and_Last_Result"]
Registration = data["Registration"]
Result_Sheet = data["Result_Sheet"]

# Display the title and introductory text
st.title("Academic Performance Over Time")

st.markdown("""

#### Welcome to the Academic Performance Over Time report.

This page provides an in-depth analysis of student academic performance 
trends across different sessions. The visualizations and metrics 
here are designed to help you understand the following aspects:

1. **Average GPA and CGPA by Session**: Track the average GPA and CGPA 
of students for each academic session to observe performance trends over time.

2. **Trend of Number of Students by CGPA Classification**: Analyze how the 
distribution of students across different CGPA classifications changes from 
one session to another.

3. **Course Performance**: Evaluate the performance of students in various 
courses and observe trends in their academic achievements.

4. **Number of Students per Session by CGPA and Classification**: Get 
insights into the number of students in each session categorized by 
their CGPA and classification.

Additionally, you can use the interactive slicers to filter the data based 
on CGPA classification, semester, and academic level. This flexibility 
allows you to focus on specific segments of the data and gain more targeted insights.

Explore the data to uncover trends, identify areas for improvement, and celebrate achievements. The visualizations and filters will assist you in making data-driven decisions to enhance academic performance.
""")


# Data Visualization
st.write("# Visualization")

st.write("<br><br>", unsafe_allow_html=True)


df_academic = Academic_Performance.copy()
df_result = Result_Sheet.copy()

# Ensure the data types of columns that will be used for merging are the same
df_academic['Session'] = df_academic['Session'].astype(str)
df_result['Session'] = df_result['Session'].astype(str)
df_academic['Matric_Number'] = df_academic['Matric_Number'].astype(str)
df_result['Matric_Number'] = df_result['Matric_Number'].astype(str)

# Merge the Academic_Performance and Result_Sheet DataFrames using Matric_Number and Session
df_merged = pd.merge(df_academic, df_result[['Matric_Number', 'Session', 'Level']], on=['Matric_Number', 'Session'], how='left')

# Define the session order and CGPA classification order
session_order = [
    '1990-1991', '1991-1992', '1992-1993', '1993-1994', '1994-1995',
    '1995-1996', '1996-1997', '1997-1998', '1999-2000', '2000-2001',
    '2001-2002', '2002-2003', '2003-2004', '2004-2005', '2005-2006',
    '2007-2008', '2008-2009', '2009-2010', '2010-2011'
]

cgpa_order = ['First Class', 'Second Class Upper', 'Second Class Lower', 'Third Class', 'Pass', 'Fail']
semester_order = ['1', '2']
level_order = ['100', '200', '300', '400', '500']

# Convert relevant columns to strings for filtering consistency
df_merged['CGPA_Classification'] = df_merged['CGPA_Classification'].astype(str)
df_merged['Semester'] = df_merged['Semester'].astype(str)
df_merged['Level'] = df_merged['Level'].astype(str)

# Filters with default set to None
selected_cgpa_classes = st.multiselect('Select CGPA Classification', options=cgpa_order, default=None)
selected_semesters = st.multiselect('Select Semesters', options=semester_order, default=None)
selected_levels = st.multiselect('Select Levels', options=level_order, default=None)

# Apply filters only if selections are made
filtered_df = df_merged.copy()

if selected_cgpa_classes:
    filtered_df = filtered_df[filtered_df['CGPA_Classification'].isin(selected_cgpa_classes)]

if selected_semesters:
    filtered_df = filtered_df[filtered_df['Semester'].isin(selected_semesters)]

if selected_levels:
    filtered_df = filtered_df[filtered_df['Level'].isin(selected_levels)]

# Plot 1: Average GPA and CGPA over Sessions
avg_gpa_cgpa = filtered_df.groupby('Session').agg({
    'GPA': 'mean',
    'CGPA': 'mean'
}).reset_index()

avg_gpa_cgpa['Session'] = pd.Categorical(avg_gpa_cgpa['Session'], categories=session_order, ordered=True)
avg_gpa_cgpa = avg_gpa_cgpa.sort_values('Session')

fig1 = px.line(avg_gpa_cgpa, x='Session', y=['GPA', 'CGPA'], 
               labels={'value': 'Average', 'variable': 'Metric'},
               color_discrete_map={'GPA': '#E516D4', 'CGPA': '#E1C233'},
               title='Average GPA and CGPA Over Sessions')
fig1.update_layout(xaxis_title='Session', yaxis_title='Average Value', 
                   plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

# Plot 2: Percentage of Students in Each CGPA Classification per Session
cgpa_percentage = filtered_df.groupby(['Session', 'CGPA_Classification'])['Matric_Number'].nunique().reset_index()
total_students_per_session = cgpa_percentage.groupby('Session')['Matric_Number'].sum().reset_index()
cgpa_percentage = pd.merge(cgpa_percentage, total_students_per_session, on='Session', suffixes=('', '_total'))
cgpa_percentage['Percentage'] = (cgpa_percentage['Matric_Number'] / cgpa_percentage['Matric_Number_total']) * 100

cgpa_percentage['Session'] = pd.Categorical(cgpa_percentage['Session'], categories=session_order, ordered=True)
cgpa_percentage = cgpa_percentage.sort_values('Session')

fig2 = px.line(cgpa_percentage, x='Session', y='Percentage', color='CGPA_Classification',
               labels={'Percentage': 'Percentage of Students', 'CGPA_Classification': 'CGPA Classification'},
               #category_orders={'CGPA_Classification': cgpa_order},
               color_discrete_map={
                   'First Class': '#0BE10B',
                   'Second Class Upper': '#FF7F0E',
                   'Second Class Lower': '#FF0DE3',
                   'Third Class': '#744EC2',
                   'Pass': '#CAD626',
                   'Fail': '#105CFF',
               },
               title='Percentage of Students in Each CGPA Classification Per Session')
fig2.update_layout(xaxis_title='Session', yaxis_title='Percentage', 
                   plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

# Plot 3: Grouped Horizontal Bar Chart with Pagination and Adjustable Height
cgpa_count = filtered_df.groupby(['Session', 'CGPA_Classification'])['Matric_Number'].nunique().reset_index()

# Filter out sessions that are not in the data
valid_sessions = cgpa_count['Session'].unique()
session_order = [s for s in session_order if s in valid_sessions]

# Set categorical orders
cgpa_count['Session'] = pd.Categorical(cgpa_count['Session'], categories=session_order, ordered=True)
cgpa_count['CGPA_Classification'] = pd.Categorical(cgpa_count['CGPA_Classification'], categories=cgpa_order, ordered=True)
cgpa_count = cgpa_count.sort_values(['Session', 'CGPA_Classification'], ascending=[True, True])

# Always display the first two plots
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# Pagination logic
pagination_enabled = st.radio("Display Mode:", ('Show All', 'Use Pagination'))

if pagination_enabled == 'Use Pagination':
    # Slider to adjust the height of the plot
    plot_height = st.slider('Adjust plot height for Visibility', min_value=400, max_value=2000, value=600)
    num_sessions_per_page = st.number_input(
        'Sessions per page',
        min_value=1,
        max_value=10,
        value=5
    )

    # Initialize session state for page management if not already present
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    total_pages = len(valid_sessions) // num_sessions_per_page + (1 if len(valid_sessions) % num_sessions_per_page else 0)

    # Create a container for pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column width for layout

    with col1:
        if st.button('Previous Page'):
            if st.session_state.current_page > 1:
                st.session_state.current_page -= 1

    with col2:
        # Dropdown to select a specific page number
        selected_page = st.selectbox(
            'Select Page',
            options=list(range(1, total_pages + 1)),
            index=st.session_state.current_page - 1
        )
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page

    with col3:
        if st.button('Next Page'):
            if st.session_state.current_page < total_pages:
                st.session_state.current_page += 1

    # Calculate start and end indices for the selected page
    start_idx = (st.session_state.current_page - 1) * num_sessions_per_page
    end_idx = start_idx + num_sessions_per_page
    sessions_to_display = valid_sessions[start_idx:end_idx]

    # Filter the data for the current page's sessions
    cgpa_count_page = cgpa_count[cgpa_count['Session'].isin(sessions_to_display)]
else:
    # Slider to adjust the height of the plot
    plot_height = st.slider('Adjust plot height for Visibility', min_value=400, max_value=3000, value=1300)
    cgpa_count_page = cgpa_count



fig3 = go.Figure()

for cgpa_class in cgpa_order:
    cgpa_data = cgpa_count_page[cgpa_count_page['CGPA_Classification'] == cgpa_class]
    fig3.add_trace(go.Bar(
        y=cgpa_data['Session'],
        x=cgpa_data['Matric_Number'],
        name=cgpa_class,
        orientation='h',
        marker=dict(color={
            'First Class': '#0BE10B',
            'Second Class Upper': '#FF7F0E',
            'Second Class Lower': '#FF0DE3',
            'Third Class': '#744EC2',
            'Pass': '#CAD626',
            'Fail': '#105CFF',
        }[cgpa_class])
    ))

# Add data labels to the bars, placed outside in front of the bars
fig3.update_traces(texttemplate='%{x}', textposition='outside')
fig3.update_layout(
    title="Number of Students per Session by CGPA Classification",
    xaxis_title='Number of Students',
    yaxis_title='Session',
    barmode='group',
    yaxis=dict(
        categoryorder='array',
        categoryarray=cgpa_count_page['Session'].unique(),
        autorange='reversed',
        tickfont=dict(size=10)  # Reducing font size for Course Titles
    ),
    xaxis=dict(
        gridcolor='gray',
        showgrid=True,
        gridwidth=1,
        griddash='dot',
        zeroline=False
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=plot_height
)

# Display the bar chart plot
st.plotly_chart(fig3, use_container_width=True)
