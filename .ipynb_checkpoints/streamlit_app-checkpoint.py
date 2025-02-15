#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt

from visualizations.indicators_generator import IndicatorsGenerator
from utils import Utils

#######################
# Page configuration
st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

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
    
    # Color theme selection
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    
    # Get followers per platform
    followers_per_platform = indicators_generator.get_followers_per_platform()

    # Get engagement metrics
    engagement_metrics = indicators_generator.get_engagement_metrics()

#######################
# Dashboard Main Panel
col1, col2 = st.columns([1, 1], gap="large")

# Column 1: Followers Per Platform
with col1:
    st.markdown('##### Followers Per Platform')

    # Platform images (ensure uniform size)
    platform_base64_icon = {
        'Facebook': utils.get_base64_icon("facebook.svg"),
        'Instagram': utils.get_base64_icon("instagram.svg"),
        'YouTube': utils.get_base64_icon("youTube.svg")
    }

    # Create centered columns for platform cards
    num_platforms = len(followers_per_platform)
    platform_cols = st.columns(num_platforms, gap="large")

    # Display followers per platform as centered cards with theme-aware colors
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

# Column 2: Engagement Metrics
with col2:
    st.markdown('##### Engagement Metrics')

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
    # Add Traffic Analytics Below
    # ==========================
    st.markdown("---")  # Add a separator line for better visual structure

    traffic_col1, traffic_col2 = st.columns([2, 1])

    # Updated traffic data with YouTube
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
        # Create a donut chart
        fig, ax = plt.subplots(figsize=(4, 4))  # Slightly increased size for better clarity
        sizes = [v[1] for v in traffic_data.values()]
        labels = list(traffic_data.keys())
        colors = [v[2] for v in traffic_data.values()]

        wedges, texts, autotexts = ax.pie(
            sizes, labels=None, colors=colors, autopct='%1.0f%%',  # Show percentages
            wedgeprops={"edgecolor": "white", "linewidth": 2},
            startangle=140,
            textprops={'fontsize': 12, 'color': 'black', 'weight': 'bold'}  # Ensures visibility
        )

        # Draw center circle to create a donut effect
        center_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(center_circle)

        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

        # Centralize the donut chart
        plt.subplots_adjust(left=0.3, right=0.7, top=0.8, bottom=0.2)

        # Display in Streamlit
        st.pyplot(fig)