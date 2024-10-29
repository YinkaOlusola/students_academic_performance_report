import numpy as np
import pandas as pd
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


# Title for the page
st.title("Course Performance")

st.write("""

#### Welcome to the Course Performance page!

This section provides a comprehensive overview of academic performance 
across various courses. Here, the following key metrics can be explored:

- **Average Scores**: View the average scores obtained in each course, 
         providing insight into overall performance trends.

- **Minimum Scores**: Identify the lowest scores recorded, helping to 
         understand areas needing improvement.

- **Maximum Scores**: Discover the highest scores achieved, celebrating 
         exceptional academic achievements.

""")

st.markdown("<br><br><br>", unsafe_allow_html=True)


# Visualizations
st.write("# Data Visualizations")

st.write("""
In the chart below, the slicers can be used to filter data by session, course, and academic level 
to get a detailed and customized view of the performance metrics. This dynamic 
feature allows you to pinpoint specific areas of interest and assess 
         performance comprehensively.

The "Show All" button displays all the Plots on one page while the "Break into Pages" divides
         the plot into pages, with the option to choose the number of items to display at once.

Adjust the height of the plot accordingly as required for better visibility.

""")


st.markdown("<br>", unsafe_allow_html=True)


# Ensuring Level column is consistently an integer
Result_Sheet['Level'] = pd.to_numeric(Result_Sheet['Level'], errors='coerce').fillna(0).astype(int)

# Grouping the data by Course_Title to get Max, Avg, and Min Marks, rounding Avg_Mark
grouped_filtered_df = Result_Sheet.groupby('Course_Title')['Mark'].agg(
    Max_Mark='max',
    Avg_Mark=lambda x: round(x.mean()),  # Rounding Average Marks to whole numbers
    Min_Mark='min'
).reset_index()

# Sorting by Max_Mark, then Avg_Mark, then Min_Mark
grouped_filtered_df = grouped_filtered_df.sort_values(
    by=['Max_Mark', 'Avg_Mark', 'Min_Mark'],
    ascending=[False, False, False]
)

# Extracting the sorted Course_Title order
course_sort_order = grouped_filtered_df['Course_Title'].tolist()

# Melting the dataframe to have a single 'Mark_Type' column for Max, Avg, Min Marks
melted_df = pd.melt(
    grouped_filtered_df,
    id_vars=['Course_Title'],
    value_vars=['Max_Mark', 'Avg_Mark', 'Min_Mark'],
    var_name='Mark_Type',
    value_name='Mark'
)

# Defining the color mapping for the different mark categories
mark_colors = {
    'Max_Mark': '#DE6A73',
    'Avg_Mark': '#E8D166',
    'Min_Mark': '#893395'
}

# Option to display everything together or use pagination
pagination_option = st.radio(
    'Display Options:',
    options=['Show All', 'Break into Pages']
)

st.write("<br>", unsafe_allow_html=True)

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

# Grouping the filtered data by Course_Title to get Max, Avg, and Min Marks, rounding Avg_Mark
grouped_filtered_df = filtered_df.groupby('Course_Title')['Mark'].agg(
    Max_Mark='max',
    Avg_Mark=lambda x: round(x.mean()),  # Rounding Average Marks to whole numbers
    Min_Mark='min'
).reset_index()

# Sorting by Max_Mark, then Avg_Mark, then Min_Mark
grouped_filtered_df = grouped_filtered_df.sort_values(
    by=['Max_Mark', 'Avg_Mark', 'Min_Mark'],
    ascending=[False, False, False]
)

# Melting the dataframe again after filtering
melted_df = pd.melt(
    grouped_filtered_df,
    id_vars=['Course_Title'],
    value_vars=['Max_Mark', 'Avg_Mark', 'Min_Mark'],
    var_name='Mark_Type',
    value_name='Mark'
)

# Pagination logic
if pagination_option == 'Break into Pages':
    # Slider to adjust the height of the plot
    plot_height = st.slider('Adjust plot height for Visibility', min_value=100, max_value=1000, value=500)
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

    # Filtering the melted_df for the selected courses on the current page
    paginated_df = melted_df[melted_df['Course_Title'].isin(paginated_courses)]
else:
    # Slider to adjust the height of the plot
    plot_height = st.slider('Adjust plot height for Visibility', min_value=100, max_value=12000, value=6000)
    paginated_df = melted_df

# Creating the grouped horizontal bar chart
fig = go.Figure()

# Adding a trace for each Mark Type
for mark_type in ['Max_Mark', 'Avg_Mark', 'Min_Mark']:
    mark_data = paginated_df[paginated_df['Mark_Type'] == mark_type]
    fig.add_trace(go.Bar(
        y=mark_data['Course_Title'],
        x=mark_data['Mark'],
        name=mark_type.replace('_', ' '),
        marker_color=mark_colors[mark_type],
        orientation='h',
        text=mark_data['Mark'],
        textposition='outside'
    ))

# Updating layout to group bars, remove background, and customize axes
fig.update_layout(
    title='Average, Maximum, and Minimum Scores by Course',
    barmode='group',
    xaxis_title='Marks',
    yaxis_title='Course Title',
    yaxis=dict(
        categoryorder='array',
        categoryarray=paginated_df['Course_Title'].unique(),
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
    showlegend=True,
    legend_title='Mark Type',
    height=plot_height
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

