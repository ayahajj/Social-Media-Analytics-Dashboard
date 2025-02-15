import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

from utils import Utils

class IndicatorsGenerator:
    
    def __init__(self, df_posts, df_comments):
        self.df_posts = df_posts
        self.df_comments = df_comments
      
    
    # Follower Per Platform
    def get_followers_per_platform(self):
        """
        Returns a dictionary with the total number of followers per platform.
        """
        followers_per_platform = self.df_posts.groupby('platform')['followers'].max().reset_index()
        return followers_per_platform

    
    # Engagment Per Platform
    def get_engagement_metrics(self):
        """
        Returns a dictionary with the total count of likes, comments, and shares.
        """
        total_likes = self.df_posts['likes'].sum()
        total_comments = self.df_posts['comments'].sum()
        total_shares = self.df_posts['shares'].sum()
        
        engagement_metrics = {
            'likes': total_likes,
            'comments': total_comments,
            'shares': total_shares
        }
        return engagement_metrics
    
    
    
    def generate_traffic_data(self):
        """
        Generate traffic analytics data based on views for each platform.

        Returns:
            dict: {Platform: (Views, Percentage, Color)}
        """
        if self.df_posts.empty:
            return {}

        # Utils
        utils = Utils(self.df_posts, self.df_comments)

        # Aggregate total views per platform
        platform_views = self.df_posts.groupby("platform")["views"].sum()

        # Calculate total views
        total_views = platform_views.sum()
        if total_views == 0:
            return {}

        # Generate traffic data
        traffic_data = {
            platform: (views, views / total_views, utils.PLATFORM_COLORS.get(platform, "#999999"))
            for platform, views in platform_views.items()
        }

        return traffic_data

    
    
    