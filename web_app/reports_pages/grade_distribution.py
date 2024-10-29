import streamlit as st
from data_loader import load_data
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Loading the data
data = load_data()

# Passing the Data into Variables
Academic_Performance = data["Academic_Performance"]
Biodata = data["Biodata"]
First_and_Last_Result = data["First_and_Last_Result"]
Registration = data["Registration"]
Result_Sheet = data["Result_Sheet"]


st.title("Grade Distribution Report")

st.markdown("""

#### Welcome to the Grade Distribution Report.
 
Here, an insightful analysis of how grades are distributed across different courses 
is presented. This page visualizes the number of students who have achieved 
various grades in each course, allowing the assessment of the overall performance and 
grading trends within the academic programs.

By exploring this data, one can identify patterns in student performance, evaluate 
the effectiveness of grading standards, and make informed decisions to support 
academic development.
            
Use the interactive charts and graphs below to gain a deeper 
understanding of the distribution of grades and uncover any notable trends.
""")


# Visualization
st.write("# Data Visualizations")



# Ensuring Level column is consistently an integer
Result_Sheet['Level'] = pd.to_numeric(Result_Sheet['Level'], errors='coerce').fillna(0).astype(int)

# Defining the sorting order for Course Titles based on the total number of distinct Matric_Number
course_sort_order = Result_Sheet.groupby('Course_Title')['Matric_Number'].nunique().sort_values(ascending=False).index.tolist()

# Define the color mapping for grades
grade_colors = {
    'A': '#0BE10B',
    'B': '#105CFF',
    'C': '#CAD626',
    'D': '#FF0DE3',
    'E': '#FF7F0E',
    'F': '#744EC2'
}

# Option to display everything together or use pagination
pagination_option = st.radio(
    'Display Options:',
    options=['Show All', 'Break into Pages']
)

# Creating filters for Course Title, Session, and Level
selected_courses = st.multiselect(
    'Select Course Titles',
    options=course_sort_order,
    default=None  # No default selection
)

selected_sessions = st.multiselect(
    'Select Sessions',
    options=sorted(Result_Sheet['Session'].unique()),
    default=None  # No default selection
)

selected_levels = st.multiselect(
    'Select Levels',
    options=sorted(Result_Sheet['Level'].unique()),
    default=None  # No default selection
)

# Ensuring that if no filters are selected, the entire dataset is used
if not selected_courses:
    selected_courses = course_sort_order
if not selected_sessions:
    selected_sessions = sorted(Result_Sheet['Session'].unique())
if not selected_levels:
    selected_levels = sorted(Result_Sheet['Level'].unique())

# Filtering the data based on user selection
filtered_df = Result_Sheet[
    (Result_Sheet['Course_Title'].isin(selected_courses)) &
    (Result_Sheet['Session'].isin(selected_sessions)) &
    (Result_Sheet['Level'].isin(selected_levels))
]

# Grouping the data by Course_Title and Grade and count distinct Matric_Number
grouped_filtered_df = filtered_df.groupby(['Course_Title', 'Grade'])['Matric_Number'].nunique().reset_index()
grouped_filtered_df.columns = ['Course_Title', 'Grade', 'Distinct_Students']

# Sorting the data: first by Course_Title, then by Distinct_Students within each Course_Title
grouped_filtered_df['Course_Title'] = pd.Categorical(grouped_filtered_df['Course_Title'], categories=course_sort_order, ordered=True)
grouped_filtered_df = grouped_filtered_df.sort_values(['Course_Title', 'Distinct_Students'], ascending=[True, False])

# Pagination logic
if pagination_option == 'Break into Pages':
    items_per_page = st.number_input(
        'Number of Items per Page',
        min_value=1,
        max_value=len(course_sort_order),
        value=10
    )

    # Initialize session state for page management if not already present
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    total_pages = len(course_sort_order) // items_per_page + (1 if len(course_sort_order) % items_per_page else 0)

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
    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paginated_courses = course_sort_order[start_idx:end_idx]

    # Filtering the grouped_filtered_df for the selected courses on the current page
    paginated_df = grouped_filtered_df[grouped_filtered_df['Course_Title'].isin(paginated_courses)]
else:
    paginated_df = grouped_filtered_df

# Creating the grouped horizontal bar chart
fig = go.Figure()

# Adding a trace for each Grade
for grade in ['A', 'B', 'C', 'D', 'E', 'F']:
    grade_data = paginated_df[paginated_df['Grade'] == grade]
    fig.add_trace(go.Bar(
        y=grade_data['Course_Title'],
        x=grade_data['Distinct_Students'],
        name=grade,
        marker_color=grade_colors[grade],
        orientation='h',
        text=grade_data['Distinct_Students'],
        textposition='outside'
    ))

# Creating a slider to adjust the height of the plot
plot_height = st.slider('Adjust plot height for Visibility', min_value=100, max_value=25000, value=12000)

# Updating layout to group bars, remove background, and customize axes
fig.update_layout(
    barmode='group',
    title="Distribution of Grades by Course",
    xaxis_title='Number of Students',
    yaxis_title='Course Title',
    yaxis=dict(
        categoryorder='array',
        categoryarray=paginated_df['Course_Title'].unique(),
        autorange='reversed',
        tickfont=dict(size=10)
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
    showlegend=True,
    legend_title='Grade',
    height=plot_height,
    # margin=dict(l=50, r=50, t=50, b=50)
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
