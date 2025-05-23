#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from social_media_scraper.Preprocess.pre_process import PreProcess
from visualizations.indicators_generator import IndicatorsGenerator
from utils import Utils
import subprocess
import time
import threading
import os
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import constants

def run_scraper(wait=False):
    """Run Scrapy spider. If wait=True, block until it finishes."""
    def scrape():
        try:
            # Create lock file to indicate Scrapy is running
            open(constants.SCRAPE_THREAD_LOCK_FILE, "w").close()
          
            print("\n\n", "Scraper Run Started...", "\n\n")
            time.sleep(5)
            if constants.IS_SIMULATE_SCRAPE == False:
                subprocess.run(["scrapy", "crawl", "social_media_spider"], cwd=constants.SCRAPE_PROCESS_EXECUTE_PATH)
            
            print("\n\n", "Scraper Run Finished...", "\n\n")
            time.sleep(1)
            
            print("\n\n", "Preprocessing Started...", "\n\n")
            time.sleep(1)
            
            preprocess_data()  # Run preprocessing immediately after scraping
            
            print("\n\n", "Preprocessing Ended...", "\n\n")
            time.sleep(1)
            
            set_last_scrape_time()  # Update last scrape time file
           
        finally:
            if os.path.exists(constants.SCRAPE_THREAD_LOCK_FILE):
                os.remove(constants.SCRAPE_THREAD_LOCK_FILE)  # Remove lock file after completion
    
    if is_scraper_running():
        print("\n\n", "Scraper Already Running...", "\n\n")
        return  # Prevent duplicate execution if scraper already running
    
    if wait:
        print("\n\n", "Running Scraper for the first time...", "\n\n")
        time.sleep(1)
        scrape()  # Run synchronously (blocking) for first run
    else:
        print("\n\n", "Running Scraper in the background thread...", "\n\n")
        time.sleep(1)
        threading.Thread(target=scrape, daemon=True).start()  # Run asynchronously


def get_last_scrape_time():
    """Returns last scrape timestamp, or None if not found."""
    if os.path.exists(constants.LAST_SUCCESSFUL_SCRAPE_TIME_FILE):
        with open(constants.LAST_SUCCESSFUL_SCRAPE_TIME_FILE, "r") as f:
            return float(f.read().strip())
    return None


def set_last_scrape_time():
    """Stores the current timestamp as the last scrape time."""
    with open(constants.LAST_SUCCESSFUL_SCRAPE_TIME_FILE, "w") as f:
        f.write(str(time.time()))


def is_scraper_running():
    """Checks if the scraper is already running."""
    return os.path.exists(constants.SCRAPE_THREAD_LOCK_FILE)
  
  
def scraper_background_task():
    """Background thread that runs Scrapy every 30 minutes."""
    while True:
        last_scrape = get_last_scrape_time()
        current_time = time.time()
        
        print("\n\n", "Background Thread Check..." + str(current_time - last_scrape) + "/ " + str(constants.SCRAPE_DATA_INTERVAL_MIN*60) + " " + str(is_scraper_running()), "\n\n")
        
        if last_scrape is None or ((current_time - last_scrape) > (constants.SCRAPE_DATA_INTERVAL_MIN * 60) and is_scraper_running() == False):
            print("\n\n", "Background Thread Runs Scraper...", "\n\n")
            run_scraper()   # Run scraper only if not running
        
        time.sleep(60)      # Check every 1 minute


def preprocess_data():
    """Clean and transform raw data after scraping."""
    try:
        pre_process = PreProcess()
        pre_process.do_preprocessing()
    except Exception as e:
        print("\n\n", f"Preprocessing error: {e}", "\n\n")
        st.error(f"Preprocessing error: {e}")


#######################
# Page configuration
st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
# Manage Scraper
#######################

# Run first Scrapy execution (blocking) if data does not exist
if not os.path.exists(constants.POSTS_DATA_FILE_PATH):
    st.warning("🚀 Collecting data for the first time. Please wait...")
    run_scraper(wait=True)  # Wait for first scrape to finish
    st.rerun()

# Start Scraper Background Task (Runs Once)
if "scraper_thread" not in st.session_state:
    scraper_thread = threading.Thread(target=scraper_background_task, daemon=True)
    scraper_thread.start()
    st.session_state["scraper_thread"] = scraper_thread

#######################
# Load data
#######################

# Load data
df_posts = pd.DataFrame()

try:
    df_posts = pd.read_excel(constants.POSTS_DATA_FILE_PATH)

except Exception as e:
    st.stop()  # Stop execution if the file is missing

# Convert 'date' and 'comment_date' columns to datetime
df_posts['date'] = pd.to_datetime(df_posts['date'])

# Utils
utils = Utils(df_posts)

# Indicators Generator
indicators_generator = IndicatorsGenerator(df_posts)

#######################
# Sidebar
#######################
with st.sidebar:
    st.title('📊 Social Media Analytics Dashboard')
    
    # # Extract unique dates from posts and comments
    # post_dates = df_posts.loc[df_posts['date'].notna(), 'date'].dt.date.unique()
    
    # # Combine and sort unique dates
    # all_dates = sorted(list(set(post_dates)))
    
    # # Date selection
    # selected_date = st.selectbox('Select a date', all_dates)
    
    # # Filter data based on selected date
    # df_selected_date_posts = df_posts[df_posts['date'].dt.date == selected_date]
    
#######################
# Dashboard Main Panel
col1, col2 = st.columns([1, 1], gap="large")
#######################

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
        'Youtube': utils.get_base64_icon("Youtube.svg")
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
                        {row.formatted_followers}
                    </h4>
                </div>
                """,
                unsafe_allow_html=True
            )

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
                        {value}
                    </h4>
                </div>
                """,
                unsafe_allow_html=True
            )

# ==========================
# Most Active Times Plot - Traffic
# ==========================

st.markdown("")  # Add a separator line
st.markdown("---")  # Add a separator line

col1, col2 = st.columns([1, 1], gap="large")

# Column 1: Most Active Times Plot
with col1:
   
    # Add Most Active Times Plot below the traffic data
    st.markdown("### Most Active Times")

    if not df_posts.empty:
        active_times = indicators_generator.generate_most_active_days(start_date='2020-01-01', end_date='2030-01-01', plot=False)

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

# Column 2: Traffic
with col2:    
    
    # ==========================
    # Traffic
    # ==========================

    traffic_col1, traffic_col2 = st.columns([2, 1], gap="small")

    # Get traffic data
    traffic_data = indicators_generator.generate_traffic_data()
    
    with traffic_col1:
        st.markdown("### Traffic")
        st.markdown("")
        for platform, (count, percentage, color) in traffic_data.items():
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;margin-left: 25px;">
                    <span style="width: 10px; height: 10px; background-color: {color}; border-radius: 50%; display: inline-block; margin-right: 10px;"></span>
                    <strong>{platform}</strong> &nbsp; {count:,} <span style="color: green;">({int(percentage * 100)}%)</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with traffic_col2:
        # Create donut chart
        fig, ax = plt.subplots(figsize=(5, 5))
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
        plt.subplots_adjust(left=0.3, right=0.7, top=0.85, bottom=0.2)

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
    

# ==========================
# Engagement Across Platforms, Engagement Type Distribution, Followers gained/lost, Follower Growth Rate
# ==========================
st.markdown("---")  # Add a separator line

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### Engagement Across Platforms")
    indicators_generator.generate_engagement_across_platforms()
with col2:
    st.markdown("### Engagement Type Distribution")
    indicators_generator.generate_engagement_type_distribution()

st.markdown("---")  # Add a separator line

col1 = st.columns(1)[0]

with col1:
    st.markdown("### Followers gained/lost")
    indicators_generator.plot_followers_comparison()

st.markdown("---")  # Add a separator line

col1 = st.columns(1)[0]

with col1:
    st.markdown("### Follower Growth Rate")
    indicators_generator.plot_follower_absolute_growth()

# ==========================
# Reach, Impressions, Sentiment, Top Posts, Engagement Heatmap by Time
# ==========================

st.markdown("---")  # Add a separator line

st.markdown("### Post Reach and Impressions by Platform")

# Display reach and impressions
col1, col2 = st.columns(2)
with col1:
    indicators_generator.plot_reach_by_platform()

with col2:
    indicators_generator.plot_impressions_by_platform()

# Display sentiment analysis
st.markdown("---")
st.markdown("### Average Sentiment by Platform")
sentiment_by_platform = indicators_generator.get_sentiment_by_platform()
if sentiment_by_platform is not None:
    st.dataframe(sentiment_by_platform)
else:
    st.warning("No comments data available for sentiment analysis.")

# Display top 10 liked posts
st.markdown("---")
st.markdown("### Top 10 Liked Posts")
indicators_generator.plot_top_10_liked_posts()

# Display top 10 shared posts
st.markdown("---")
st.markdown("### Top 10 Shared Posts")
indicators_generator.plot_top_10_shared_posts()

# Display engagement heatmap by time
st.markdown("---")
st.markdown("### Best Time to Post (Engagement Heatmap)")
indicators_generator.plot_engagement_heatmap_by_time()

# ==============================================================================
# Dashboard Refreshing every specified DASHBOARD_REFRESH_INTERVAL_MIN
# ==============================================================================

print("\n\n", "Dashboard Refreshed ...", "\n\n")
st_autorefresh(interval= constants.DASHBOARD_REFRESH_INTERVAL_MIN * 60 * 1000, limit=None, key="fizzbuzzcounter")

# ==========================
# 
# ==========================
