import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import Utils

class IndicatorsGenerator:
    
    def __init__(self, df_posts, df_comments):
        self.df_posts = df_posts
        self.df_comments = df_comments
    
    # Returns a dictionary with the total number of followers per platform.
    def get_followers_per_platform(self):
        followers_per_platform = self.df_posts.groupby('platform')['followers'].max().reset_index()
        return followers_per_platform

    # Returns a dictionary with the total count of likes, comments, and shares.
    def get_engagement_metrics(self):
        total_likes = self.df_posts['likes'].sum()
        total_comments = self.df_posts['comments'].sum()
        total_shares = self.df_posts['shares'].sum()
        
        engagement_metrics = {
            'likes': total_likes,
            'comments': total_comments,
            'shares': total_shares
        }
        return engagement_metrics
    
    # Generate traffic analytics data based on views for each platform and 
    # return dict: {Platform: (Views, Percentage, Color)}
    def generate_traffic_data(self):
        if self.df_posts.empty:
            return {}

        utils = Utils(self.df_posts, self.df_comments)

        # total views per platform
        platform_views = self.df_posts.groupby("platform")["views"].sum()

        # Calculate total views
        total_views = platform_views.sum()
        if total_views == 0:
            return {}

        # Generate traffic data
        traffic_data = {
            platform: (views, views / total_views, utils.PLATFORM_COLORS.get(platform, "#000000"))
            for platform, views in platform_views.items()
        }

        return traffic_data

    
    # Generates and displays a heatmap of engagement data using Plotly.
    # Parameters:
    # heatmap_data (pd.DataFrame): A DataFrame containing engagement data with columns 'platform', 'day', and 'engagement'.
    # Returns: None: Displays the heatmap in a Streamlit application.
    def generate_engagement_heatmap_data(self):
        if self.df_posts.empty:
            return None

        # Extract day from the date
        self.df_posts['day'] = pd.to_datetime(self.df_posts['date']).dt.date

        # Calculate total engagement (likes + comments + shares)
        self.df_posts['engagement'] = self.df_posts['likes'] + self.df_posts['comments'] + self.df_posts['shares']

        # Group by platform and day, then calculate total engagement
        heatmap_data = self.df_posts.groupby(['platform', 'day'])['engagement'].sum().reset_index()

        return heatmap_data
    
    # Generates engagement heatmap data by calculating total engagement per platform per day.
    # Parameters: df_posts (pd.DataFrame): A DataFrame containing post data with columns 'date', 'platform', 'likes', 
    # 'comments', and 'shares'.
    #  Returns: pd.DataFrame: A DataFrame with aggregated engagement data, including 'platform', 'day', and 'engagement'.
    def plot_engagement_heatmap(self, heatmap_data):
        if heatmap_data is None or heatmap_data.empty:
            st.warning("No data available to generate the heatmap.")
            return

        # Pivot the data for the heatmap
        heatmap_pivot = heatmap_data.pivot(index='platform', columns='day', values='engagement')

        # Define custom colors for each platform
        platform_colors = {
            'YouTube': 'red',
            'Facebook': 'blue',
            'Instagram': 'magenta'
        }

        # Create the heatmap using Plotly Graph Objects
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,  # Engagement values
            x=heatmap_pivot.columns,  # Days
            y=heatmap_pivot.index,    # Platforms
            colorscale=[[0, 'white'], [1, platform_colors['YouTube']]],  # Custom colors
            hoverongaps=False,
            colorbar=dict(title="Engagement")
        ))

            # Customize layout
        fig.update_layout(
            title="",
            xaxis_title="Day",
            yaxis_title="Platform",
            xaxis=dict(tickformat="%Y-%m-%d"),  # Format date on x-axis
            yaxis=dict(autorange="reversed")     # Reverse y-axis to match typical heatmap orientation
        )

        # Display in Streamlit
        st.plotly_chart(fig)
        
        
        
        