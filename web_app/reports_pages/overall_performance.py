import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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

#### Welcome to the Overall Performance page.
         
This section provides an insightful analysis of the academic achievements of 
students across various sessions. The primary focus here is on the number of 
graduating students categorized by their final Cumulative Grade Point Average 
         (CGPA) classifications.

In this report, you can explore:

- **Number of Graduating Students**: View the count of students 
who have graduated based on different CGPA classifications.

- **CGPA Classification**: Understand the distribution of students 
across various performance brackets, helping to gauge the overall 
academic performance of the student body.

- **Session Filter**: Use the slicer to filter the data by specific 
academic sessions to view performance trends over time.

Interact with the report to gain a comprehensive understanding of academic 
performance and track the progress of graduating students by their final CGPA.
""")


df = First_and_Last_Result.copy()

# Define the session order and CGPA classification order
session_order = [
    '1990-1991', '1991-1992', '1992-1993', '1993-1994', '1994-1995',
    '1995-1996', '1996-1997', '1997-1998', '1999-2000', '2000-2001',
    '2001-2002', '2002-2003', '2003-2004', '2004-2005', '2005-2006',
    '2007-2008', '2008-2009', '2009-2010', '2010-2011'
]

cgpa_order = ['First Class', 'Second Class Upper', 'Second Class Lower', 'Third Class', 'Pass', 'Fail']

# Replace session values as per the requirement (modify this if needed for correct session values)
df['Last_Session'] = df['Last_Session'].replace({
    '97/98': '1997-1998',
    '90-92': '1990-1991'
})

# Filter by Session
selected_sessions = st.multiselect('Filter by Session:', options=session_order, default=[])

# If no sessions are selected, use all available sessions in the data
if not selected_sessions:
    selected_sessions = df['Last_Session'].unique()

# Filter the dataframe based on selected sessions
filtered_df = df[df['Last_Session'].isin(selected_sessions)]

# Ensure only sessions present in the filtered data are used
valid_sessions = filtered_df['Last_Session'].unique()
session_order = [s for s in session_order if s in valid_sessions]

# Doughnut Chart (CGPA Classification Distribution)
cgpa_distribution = filtered_df['Last_CGPA_Classification'].value_counts().reset_index()
cgpa_distribution.columns = ['CGPA_Classification', 'Count']

# Define consistent colors for the charts
color_map = {
    'First Class': '#0BE10B',
    'Second Class Upper': '#FF7F0E',
    'Second Class Lower': '#FF0DE3',
    'Third Class': '#744EC2',
    'Pass': '#CAD626',
    'Fail': '#105CFF',
}

fig_doughnut = px.pie(
    cgpa_distribution,
    values='Count',
    names='CGPA_Classification',
    title='Distribution of CGPA Classifications',
    hole=0.5,
    color='CGPA_Classification',
    color_discrete_map=color_map
)

# Update the pie chart layout
fig_doughnut.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=50, b=50, l=50, r=50)
)

# Display the doughnut chart
st.plotly_chart(fig_doughnut, use_container_width=True)

# Grouped Horizontal Bar Chart with Pagination and Adjustable Height
cgpa_count = filtered_df.groupby(['Last_Session', 'Last_CGPA_Classification'])['Matric_Number'].nunique().reset_index()
cgpa_count.columns = ['Session', 'CGPA_Classification', 'Distinct_Students']

# Sort sessions and CGPA classifications
cgpa_count['Session'] = pd.Categorical(cgpa_count['Session'], categories=session_order, ordered=True)
cgpa_count['CGPA_Classification'] = pd.Categorical(cgpa_count['CGPA_Classification'], categories=cgpa_order, ordered=True)
cgpa_count = cgpa_count.sort_values(['Session', 'CGPA_Classification'])

# Pagination logic
pagination_enabled = st.radio("Display Mode:", ('Show All', 'Break into Pages'))

if pagination_enabled == 'Break into Pages':
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

    total_pages = len(session_order) // num_sessions_per_page + (1 if len(session_order) % num_sessions_per_page else 0)

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
    sessions_to_display = session_order[start_idx:end_idx]

    # Filter the data for the current page's sessions
    cgpa_count_page = cgpa_count[cgpa_count['Session'].isin(sessions_to_display)]
else:
    # Slider to adjust the height of the plot
    plot_height = st.slider('Adjust plot height for Visibility', min_value=400, max_value=3000, value=1300)
    cgpa_count_page = cgpa_count

# Corrected Bar Chart Implementation Using plotly.graph_objects
fig3 = go.Figure()

for cgpa_class in cgpa_order:
    cgpa_data = cgpa_count_page[cgpa_count_page['CGPA_Classification'] == cgpa_class]
    fig3.add_trace(go.Bar(
        y=cgpa_data['Session'],
        x=cgpa_data['Distinct_Students'],
        name=cgpa_class,
        orientation='h',
        marker=dict(color=color_map[cgpa_class])
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
        categoryarray=session_order,
        autorange='reversed'
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
