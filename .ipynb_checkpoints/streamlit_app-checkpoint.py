#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from visualizations.indicators_generator import IndicatorsGenerator
from utils import Utils

#######################
# Page configuration
st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

# alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################
# Load data
df_posts = pd.read_csv('data/social_media_posts.csv')
df_comments = pd.read_csv('data/social_media_comments.csv')

# Convert 'date' and 'comment_date' columns to datetime
df_posts['date'] = pd.to_datetime(df_posts['date'])
df_comments['comment_date'] = pd.to_datetime(df_comments['comment_date'])

# Utils
utils = Utils(df_posts, df_comments)

# Indicators Generator
indicators_generator = IndicatorsGenerator(df_posts, df_comments)

#######################

# Sidebar
with st.sidebar:
    st.title('📊 Social Media Analytics Dashboard')
    
    # Extract unique dates from posts and comments
    post_dates = df_posts['date'].dt.date.unique()
    comment_dates = df_comments['comment_date'].dt.date.unique()
    
    # Combine and sort unique dates
    all_dates = sorted(list(set(post_dates) | set(comment_dates)))
    
    # Date selection
    selected_date = st.selectbox('Select a date', all_dates)
    
    # Filter data based on selected date
    df_selected_date_posts = df_posts[df_posts['date'].dt.date == selected_date]
    df_selected_date_comments = df_comments[df_comments['comment_date'].dt.date == selected_date]
    
#######################
# Dashboard Main Panel
col1, col2 = st.columns([1, 1], gap="large")

# Column 1: Followers Per Platform
with col1:
    # ==========================
    # Followers Per Platform
    # ==========================
    st.markdown('##### Followers Per Platform')

    # Get followers per platform
    followers_per_platform = indicators_generator.get_followers_per_platform()

    # Platform images (ensure uniform size)
    platform_base64_icon = {
        'Facebook': utils.get_base64_icon("facebook.svg"),
        'Instagram': utils.get_base64_icon("instagram.svg"),
        'YouTube': utils.get_base64_icon("youTube.svg")
    }

    # Create centered columns for platform cards
    platform_cols = st.columns(len(followers_per_platform), gap="large")

    # Display followers per platform as centered cards
    for index, row in enumerate(followers_per_platform.itertuples()):
        with platform_cols[index]:
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    background-color: var(--background-color);
                    padding: 15px;
                    border-radius: 12px;
                    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
                    width: 160px;
                    height: 150px;
                ">
                    <img src="{platform_base64_icon[row.platform]}" width="30" height="30" style="margin-bottom:5px;">
                    <h3 style="color: var(--text-color); font-size: 15px; font-weight: bold; margin-left:25px;"> 
                        {row.platform}
                    </h3>
                    <h4 style="color: var(--text-color); font-size: 18px; margin-left:20px;"> 
                        {row.followers:,}
                    </h4>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Add Most Active Times Plot below the traffic data
    st.markdown("---")  # Add a separator line
    st.markdown("### Most Active Times")
    
    if not df_posts.empty:
        active_times = indicators_generator.generate_most_active_days(start_date='2023-09-01', end_date='2023-10-20', plot=False)

    # Plot the most active days
        fig, ax = plt.subplots(figsize=(10, 4))  # Adjust the figure size for better fit
        ax.bar(active_times['day'].astype(str), active_times['post_count'], color=utils.PLATFORM_COLORS.get('Facebook', "#000000"))  # Convert days to strings for plotting
        ax.set_xlabel('Day')
        ax.set_ylabel('Number of Posts')
        ax.set_title('Most Active Days')
        ax.set_xticks(range(len(active_times)))  # Set x-ticks based on the number of days
        ax.set_xticklabels(active_times['day'].astype(str), rotation=45)  # Rotate x-axis labels for better readability
        ax.grid(axis='y')
        plt.tight_layout()  # Adjust layout to prevent label cutoff
        st.pyplot(fig)

# Column 2: Engagement Metrics
with col2:
    
    # ==========================
    # Engagement Metrics
    # ==========================
    st.markdown('##### Engagement Metrics')

    # Get engagement metrics
    engagement_metrics = indicators_generator.get_engagement_metrics()
    
    # Engagement metric icons using local images
    engagement_metrics_data = [
        ("Likes", utils.get_base64_icon("likes.svg"), engagement_metrics["likes"]),
        ("Comments", utils.get_base64_icon("comments.svg"), engagement_metrics["comments"]),
        ("Shares", utils.get_base64_icon("shares.svg"), engagement_metrics["shares"])
    ]

    # Centered columns for metrics
    engagement_cols = st.columns(3, gap="large")

    # Display engagement metrics as cards
    for index, (label, icon_base64, value) in enumerate(engagement_metrics_data):
        with engagement_cols[index]:
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    background-color: var(--background-color);
                    padding: 15px;
                    border-radius: 12px;
                    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
                    width: 160px;
                    height: 150px;
                ">
                    <img src="{icon_base64}" width="30" height="30" style="margin-bottom:5px;">
                    <h3 style="color: var(--text-color); font-size: 15px; font-weight: bold; margin-left:25px;"> 
                        {label}
                    </h3>
                    <h4 style="color: var(--text-color); font-size: 18px; margin-left:20px;"> 
                        {value:,}
                    </h4>
                </div>
                """,
                unsafe_allow_html=True
            )


    # ==========================
    # Traffic
    # ==========================
    st.markdown("---")  # Add a separator line

    traffic_col1, traffic_col2 = st.columns([2, 1])

    # Get traffic data
    traffic_data = indicators_generator.generate_traffic_data()
    
    with traffic_col1:
        st.markdown("### Traffic")
        for platform, (count, percentage, color) in traffic_data.items():
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="width: 10px; height: 10px; background-color: {color}; border-radius: 50%; display: inline-block; margin-right: 10px;"></span>
                    <strong>{platform}</strong> &nbsp; {count:,} <span style="color: green;">({int(percentage * 100)}%)</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with traffic_col2:
        # Create donut chart
        fig, ax = plt.subplots(figsize=(4, 4))
        labels = list(traffic_data.keys())
        percentages = [v[1] for v in traffic_data.values()]
        colors = [v[2] for v in traffic_data.values()]

        wedges, texts, autotexts = ax.pie(
            percentages, labels=None, colors=colors, autopct='%1.0f%%',  # Show percentages
            wedgeprops={"edgecolor": "white", "linewidth": 2},
            startangle=140,
            textprops={'fontsize': 12, 'color': 'black', 'weight': 'bold'}
        )

        center_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(center_circle)

        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

        # Centralize the donut chart
        plt.subplots_adjust(left=0.3, right=0.7, top=0.8, bottom=0.2)

        # Display in Streamlit
        st.pyplot(fig)
        
# ==========================
# Engagement Heatmap
# ==========================
st.markdown("---")  # Add a separator line
st.markdown("### Engagement Heatmap by Day and Platform")


# Create a single column layout (new row)
heatmap_col = st.columns(1)[0]  # st.columns(1) returns a list with one column

with heatmap_col:
    # Generate heatmap data
    heatmap_data = indicators_generator.generate_engagement_heatmap_data()

# Ensure `day` column is of type datetime
heatmap_data['day'] = pd.to_datetime(heatmap_data['day'])

# Set a default date range for selection
date_range = st.date_input("Select Date Range", 
                           [heatmap_data['day'].min().date(), heatmap_data['day'].max().date()])

# Ensure date_range is always a list with two values
if isinstance(date_range, tuple):  # Sometimes Streamlit returns a tuple
    date_range = list(date_range)

if len(date_range) == 1:  # If only one date is selected, duplicate it to create a valid range
    start_date = date_range[0]
    end_date = date_range[0]
else:
    start_date, end_date = date_range  # Extract two values

# Convert to datetime for filtering
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter heatmap data based on the selected date range
filtered_heatmap_data = heatmap_data[
    (heatmap_data['day'] >= start_date) & (heatmap_data['day'] <= end_date)
]

# Plot the filtered heatmap
indicators_generator.plot_engagement_heatmap(filtered_heatmap_data)
    
# ==========================
# Social Likes/Reactions Plot
# ==========================
st.markdown("---")  # Add a separator line


# Create a two-column layout
col1, col2 = st.columns([1, 1], gap="large")

# First column (empty or for other content)
with col1:
    # Generate the social interactions plot
    st.markdown("### Social Likes/Reactions Over Months by Platform")
    indicators_generator.generate_social_likes_reactions_plot()
    
# Second column: Social Interactions Plot
with col2:
    st.markdown("### Posts Distribution by Content Type")
    indicators_generator.generate_comments_per_type_pie_chart()


# ==========================
# Social Reshare Plot
# ==========================
st.markdown("---")  # Add a separator line

# Create a two-column layout
col1 = st.columns(1)[0]

# First column (empty or for other content)
with col1:
    # Generate the social interactions plot
    st.markdown("### Social Resharing Over Months by Platform")
    indicators_generator.generate_social_resharing_plot()
    

    