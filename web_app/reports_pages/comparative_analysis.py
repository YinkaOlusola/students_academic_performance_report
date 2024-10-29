import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math
from data_loader import load_data

# Loading the data
data = load_data()

# Passing the Data into Variables
Academic_Performance = data["Academic_Performance"]
Biodata = data["Biodata"]
First_and_Last_Result = data["First_and_Last_Result"]
Registration = data["Registration"]
Result_Sheet = data["Result_Sheet"]


st.title("Comparative Analysis")

st.write("""
#### Welcome to the Comparative Analysis Report.
 
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


st.write("<br><br>", unsafe_allow_html=True)


# Data Visualization
st.write("# Visualization - 1")

st.write("<br><br>", unsafe_allow_html=True)


# Merging the dataframes
merged_df = pd.merge(Academic_Performance, Registration, 
                     on=['Matric_Number', 'Session', 'Semester'], 
                     how='inner')

# Sidebar - Semester Slicer
semester = st.sidebar.selectbox("Select Semester:", options=['All'] + merged_df['Semester'].unique().tolist())

# Filter the data based on the selected Semester
if semester != 'All':
    filtered_df = merged_df[merged_df['Semester'] == semester]
else:
    filtered_df = merged_df

# Group sessions by sets of 2 or 3
sessions = sorted(filtered_df['Session'].unique())
sessions_per_page = 2  # Adjust this to 3 if you want 3 sessions per page
total_pages = math.ceil(len(sessions) / sessions_per_page)

# Initialize session state for pagination
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

# Sidebar - Pagination Controls
pagination_cols = st.sidebar.columns([1, 2, 1])
with pagination_cols[0]:
    if st.button("Back"):
        if st.session_state.current_page > 1:
            st.session_state.current_page -= 1

with pagination_cols[1]:
    st.session_state.current_page = st.number_input(
        "Page", min_value=1, max_value=total_pages, 
        value=st.session_state.current_page, step=1, format="%d"
    )

with pagination_cols[2]:
    if st.button("Next"):
        if st.session_state.current_page < total_pages:
            st.session_state.current_page += 1

# Sidebar - Slider for adjusting plot height
plot_height = st.sidebar.slider("Adjust Plot Height:", min_value=200, max_value=1000, value=300)

# Determine the sessions to display on the current page
start_idx = (st.session_state.current_page - 1) * sessions_per_page
end_idx = start_idx + sessions_per_page
current_sessions = sessions[start_idx:end_idx]

# Filter the data for the current page sessions
page_df = filtered_df[filtered_df['Session'].isin(current_sessions)]

# CGPA Classification order and colors
classification_order = ['First Class', 'Second Class Upper', 'Second Class Lower', 'Third Class', 'Pass', 'Fail']
classification_colors = {
    'First Class': '#0BE10B',
    'Second Class Upper': '#FF7F0E',
    'Second Class Lower': '#FF0DE3',
    'Third Class': '#744EC2',
    'Pass': '#CAD626',
    'Fail': '#105CFF'
}

# Plotting the charts for each level
levels = sorted(page_df['Level'].unique())
figures = []

for level in levels:
    level_df = page_df[page_df['Level'] == level]
    grouped_df = level_df.groupby(['Session', 'CGPA_Classification']).agg(
        DistinctStudentCount=('Matric_Number', 'nunique')
    ).reset_index()

    # Create Plotly bar chart for each level
    fig = go.Figure()
    for classification in classification_order:
        class_df = grouped_df[grouped_df['CGPA_Classification'] == classification]
        fig.add_trace(go.Bar(
            x=class_df['DistinctStudentCount'],
            y=class_df['Session'],
            name=classification,
            orientation='h',
            marker_color=classification_colors[classification],
            text=class_df['DistinctStudentCount'],  # Add data labels
            textposition='outside'  # Position labels automatically
        ))

    fig.update_layout(
        barmode='group',
        height=plot_height,
        title=f"{level} Level - CGPA Classification Distribution",
        xaxis_title="Distinct Student Count",
        yaxis_title="Session",
        legend_title="CGPA Classification",
        xaxis=dict(tickformat='d'),
        yaxis=dict(categoryorder='category ascending',
                   autorange='reversed'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    figures.append(fig)

# Display all four charts on the current page
for fig in figures:
    st.plotly_chart(fig)





st.write("<br><br><br><br><br>", unsafe_allow_html=True)

# Data Visualization
st.write("# CGPA Analysis")



# Plot 1: Average of First CGPA across Session
avg_first_cgpa = First_and_Last_Result.groupby('First_Session')['First_CGPA'].mean().reset_index()

fig1 = px.line(avg_first_cgpa, 
               x='First_Session', 
               y='First_CGPA', 
               title="Average of First CGPA across Session")

fig1.update_traces(line=dict(color='#E669B9'))
fig1.update_layout(xaxis_tickangle=-45,
                   xaxis_title='First Session',
                   yaxis_title='Average First CGPA',
                   xaxis=dict(tickfont=dict(size=12)))

# Plot 2: Average of Last CGPA across Session
avg_last_cgpa = First_and_Last_Result.groupby('Last_Session')['Last_CGPA'].mean().reset_index()

fig2 = px.line(avg_last_cgpa, 
               x='Last_Session', 
               y='Last_CGPA', 
               title="Average of Final Result across Session")

fig2.update_traces(line=dict(color='#E669B9'))
fig2.update_layout(xaxis_tickangle=-45,
                   xaxis_title='Last Session',
                   yaxis_title='Average Last CGPA',
                   xaxis=dict(tickfont=dict(size=12)))

# Plot 3: Scatter Plot of Last CGPA vs First CGPA
fig3 = px.scatter(First_and_Last_Result, 
                  x='First_CGPA', 
                  y='Last_CGPA', 
                  title="Relationship between Last CGPA and First CGPA",
                  color_discrete_sequence=['#E669B9'])

fig3.update_layout()

# Display plots in Streamlit
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

