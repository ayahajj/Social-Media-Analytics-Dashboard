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
    
    def __init__(self, df_posts):
        self.df_posts = df_posts
        self.utils = Utils(self.df_posts)
    
    
    # Returns a dictionary with the total number of followers per platform.
    def get_followers_per_platform(self):
        followers_per_platform = self.df_posts.groupby('platform')['followers'].max().reset_index()
        followers_per_platform['formatted_followers'] = followers_per_platform['followers'].apply(self.utils.format_values)
        return followers_per_platform


    # Returns a dictionary with the total count of likes, comments, and shares.
    def get_engagement_metrics(self):
        total_likes = self.df_posts['likes'].sum()
        total_comments = self.df_posts['comments'].sum()
        total_shares = self.df_posts['shares'].sum()
        
        engagement_metrics = {
            'likes': self.utils.format_values(total_likes),
            'comments': self.utils.format_values(total_comments),
            'shares': self.utils.format_values(total_shares)
        }
        return engagement_metrics
    
    
    # Analyzes and returns the most active days based on user post activity.
    # start_date (str, optional): Start date for filtering posts (format: 'YYYY-MM-DD'). Defaults to None.
    # end_date (str, optional): End date for filtering posts (format: 'YYYY-MM-DD'). Defaults to None.
    # timezone (str, optional): Timezone to convert the timestamps to. Defaults to 'UTC'.
    # plot (bool, optional): Whether to plot the results. Defaults to False.
    # returns: DataFrame: A pandas DataFrame containing the number of posts per day.
    def generate_most_active_days(self, start_date=None, end_date=None, timezone='UTC', plot=False):
        if self.df_posts.empty:
            return None

        # Work with a copy to avoid modifying self.df_posts
        df_copy = self.df_posts.copy()

        # Convert 'date' column to datetime and set timezone
        df_copy['date'] = pd.to_datetime(df_copy['date']).dt.tz_localize(timezone)

        # Filter by date range if provided
        if start_date and end_date:
            mask = (df_copy['date'] >= start_date) & (df_copy['date'] <= end_date)
            df_copy = df_copy.loc[mask]

        # Extract day from the timestamp
        df_copy['day'] = df_copy['date'].dt.date  # Use dt.date for specific dates

        # Count posts per day
        active_days = df_copy.groupby('day').size().reset_index(name='post_count')

        # Sort by post count in descending order
        active_days = active_days.sort_values(by='post_count', ascending=False)

        # Plot the results if requested
        if plot:
            self._plot_most_active_days(active_days)

        return active_days


    # Generate traffic analytics data based on views for each platform and 
    # return dict: {Platform: (Views, Percentage, Color)}
    def generate_traffic_data(self):
        if self.df_posts.empty:
            return {}
        
        df_copy = self.df_posts.copy()
        
        # Calculate total engagement (sum of views, comments, shares, and likes) per platform
        df_copy['total_engagement'] = (
            self.df_posts['comments'] + 
            self.df_posts['shares'] + 
            self.df_posts['likes']
        )

        platform_engagement = df_copy.groupby("platform")["total_engagement"].sum()

        # Calculate total engagement across all platforms
        total_engagement = platform_engagement.sum()
        if total_engagement == 0:
            return {}

        # Generate traffic data
        traffic_data = {
            platform: (
                engagement,  # Total engagement for the platform
                engagement / total_engagement,  # Percentage of total engagement
                self.utils.PLATFORM_COLORS.get(platform, "#000000")  # Platform color
            )
            for platform, engagement in platform_engagement.items()
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
            'Youtube': 'red',
            'Facebook': 'blue',
            'Instagram': 'magenta'
        }

        # Create the heatmap using Plotly Graph Objects
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,  # Engagement values
            x=heatmap_pivot.columns,  # Days
            y=heatmap_pivot.index,    # Platforms
            colorscale=[[0, 'white'], [1, platform_colors['Youtube']]],  # Custom colors
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
        
        
    # Generates a plot showing likes_reactions over months for different platforms.
    # Each platform will have one curve with custom colors.
    def generate_social_likes_reactions_plot(self):     
            
        # Ensure 'date' column is datetime
        self.df_posts['date'] = pd.to_datetime(self.df_posts['date'])

        # Extract month and year from the date
        self.df_posts['month'] = self.df_posts['date'].dt.to_period('M')

        # Aggregate data by month and platform
        aggregated_data = self.df_posts.groupby(['month', 'platform']).agg({
            'likes': 'sum',
            'comments': 'sum'
        }).reset_index()

        # Calculate total interactions (sum of likes, comments, and shares)
        aggregated_data['total_interactions'] = (
            aggregated_data['likes'] + aggregated_data['comments']
        )

        # Convert 'month' back to string for plotting
        aggregated_data['month'] = aggregated_data['month'].astype(str)

        # Define custom colors for each platform
        platform_colors = {
            'Youtube': self.utils.PLATFORM_COLORS.get('Youtube', "#000000"),  # Red
            'Facebook': self.utils.PLATFORM_COLORS.get('Facebook', "#000000"),  # Facebook Blue
            'Instagram': self.utils.PLATFORM_COLORS.get('Instagram', "#000000"),  # Twitter Blue
            # Add more platforms and colors as needed
        }

        # Plot the data
        plt.figure(figsize=(12, 10))
        for platform in aggregated_data['platform'].unique():
            platform_data = aggregated_data[aggregated_data['platform'] == platform]
            plt.plot(
                platform_data['month'], 
                platform_data['total_interactions'], 
                label=platform, 
                marker='o', 
                color=platform_colors.get(platform, '#000000')  # Default to black if platform not in the dictionary
            )

        # Customize the plot
        plt.xlabel('Month')
        plt.ylabel('Total Likes & Comments')
        plt.title('Total Social Likes & Comments Over Months by Platform')
        plt.legend(title='Platform')
        plt.grid(True)
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()

        # Show the plot in Streamlit
        st.pyplot(plt)

        
    # Generates a pie chart showing the distribution of comments by content type (e.g., video, photo, Text).
    def generate_comments_per_type_pie_chart(self):

        comments_by_type = self.df_posts.groupby('content_type')['post_id'].count().reset_index(name='comment_count')

        # Calculate percentages
        comments_by_type['percentage'] = (comments_by_type['comment_count'] / comments_by_type['comment_count'].sum()) * 100

        # Define custom colors for each content type
        content_type_colors = {
            'image': '#FF0000',  # Red
            'video': '#3b5998',  # Facebook Blue
            'text': '#1DA1F2',  # Twitter Blue
        }

        # Plot the pie chart
        plt.figure(figsize=(8, 4))
        plt.pie(
            comments_by_type['comment_count'],
            labels=comments_by_type['content_type'],
            autopct='%1.1f%%',  # Show percentages
            colors=[content_type_colors.get(ct, '#000000') for ct in comments_by_type['content_type']],  # Custom colors
            startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}  # Add white edges to slices
        )

        # Add a title
        # plt.title('Posts Distribution by Content Type')

        # Show the plot in Streamlit
        st.pyplot(plt)
 
 
    # Generates a plot showing total social sharing (sum of shares) over months for different platforms.
    # Each platform will have one curve with custom colors.
    def generate_social_resharing_plot(self):
        utils = Utils(self.df_posts)
            
        # Ensure 'date' column is datetime
        self.df_posts['date'] = pd.to_datetime(self.df_posts['date'])

        # Extract month and year from the date
        self.df_posts['month'] = self.df_posts['date'].dt.to_period('M')

        # Aggregate data by month and platform
        aggregated_data = self.df_posts.groupby(['month', 'platform']).agg({
           
            'shares': 'sum'
        }).reset_index()

        # Calculate total interactions (sum of likes, comments, and shares)
        aggregated_data['total_interactions'] = (
           aggregated_data['shares']
        )

        # Convert 'month' back to string for plotting
        aggregated_data['month'] = aggregated_data['month'].astype(str)

        # Define custom colors for each platform
        platform_colors = {
            'Youtube': self.utils.PLATFORM_COLORS.get('Youtube', "#000000"),  # Red
            'Facebook': self.utils.PLATFORM_COLORS.get('Facebook', "#000000"),  # Facebook Blue
            'Instagram': self.utils.PLATFORM_COLORS.get('Instagram', "#000000"),  # Twitter Blue
            # Add more platforms and colors as needed
        }

        # Plot the data
        plt.figure(figsize=(10, 6))
        for platform in aggregated_data['platform'].unique():
            platform_data = aggregated_data[aggregated_data['platform'] == platform]
            plt.plot(
                platform_data['month'], 
                platform_data['total_interactions'], 
                label=platform, 
                marker='o', 
                color=platform_colors.get(platform, '#000000')  # Default to black if platform not in the dictionary
            )

        # Customize the plot
        plt.xlabel('Month')
        plt.ylabel('Total Shares')
        plt.title('Total Social Shares Over Months by Platform')
        plt.legend(title='Platform')
        plt.grid(True)
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()

        # Show the plot in Streamlit
        st.pyplot(plt)
        


    
    # New method: Calculate total reach by platform
    def get_reach_by_platform(self):
        posts_df = self.df_posts.copy()
        posts_df["total_reach"] = posts_df.apply(
            lambda row: row["views"] if row["views"] > 0 else (row["likes"] + row["comments"] + row["shares"]),
            axis=1
        )
        reach_by_platform = posts_df.groupby("platform")["total_reach"].sum().reset_index()
        return reach_by_platform

    # New method: Calculate total impressions by platform
    def get_impressions_by_platform(self):
        posts_df = self.df_posts.copy()
        posts_df["total_impressions"] = posts_df.apply(
            lambda row: row["views"] if row["views"] > 0 else (row["likes"] + row["comments"] + row["shares"]),
            axis=1
        )
        impressions_by_platform = posts_df.groupby("platform")["total_impressions"].sum().reset_index()
        return impressions_by_platform

    # New method: Calculate average sentiment by platform
    def get_sentiment_by_platform(self):
        sentiment_by_platform = self.df_posts.groupby("platform")["sentiment_score"].mean().reset_index()
        sentiment_by_platform.rename(columns={"comment_sentiment": "avg_sentiment"}, inplace=True)
        return sentiment_by_platform

    # New method: Get top 10 liked posts
    def get_top_10_liked_posts(self):
        top_10_liked_posts = self.df_posts.sort_values(by="likes", ascending=False).head(10)
        return top_10_liked_posts

    # New method: Get top 10 shared posts
    def get_top_10_shared_posts(self):
        top_10_shared_posts = self.df_posts.sort_values(by="shares", ascending=False).head(10)
        return top_10_shared_posts

    # New method: Generate engagement heatmap by hour and day of the week
    def generate_engagement_heatmap_by_time(self):
        posts_df = self.df_posts.copy()
        posts_df["hour"] = posts_df["date"].dt.hour
        posts_df["day_of_week"] = posts_df["date"].dt.day_name()
        engagement_by_time = posts_df.groupby(["day_of_week", "hour"])[["likes", "comments", "shares"]].sum().reset_index()
        engagement_by_time["total_engagement"] = engagement_by_time[["likes", "comments", "shares"]].sum(axis=1)
        heatmap_data = engagement_by_time.pivot(index="day_of_week", columns="hour", values="total_engagement")
        ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heatmap_data = heatmap_data.reindex(ordered_days)
        return heatmap_data

    # New method: Plot engagement heatmap by time
    def plot_engagement_heatmap_by_time(self):
        heatmap_data = self.generate_engagement_heatmap_by_time()
        if heatmap_data is None or heatmap_data.empty:
            st.warning("No data available to generate the heatmap.")
            return

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale="YlGnBu",
            colorbar=dict(title="Engagement")
        ))
        fig.update_layout(
            xaxis=dict(title="Hour of the Day"),
            yaxis=dict(title="Day of the Week")
        )
        st.plotly_chart(fig)

    # New method: Plot pie chart for reach by platform
    def plot_reach_by_platform(self):
        reach_by_platform = self.get_reach_by_platform()
        fig = px.pie(
            reach_by_platform,
            values="total_reach",
            names="platform",
            title="Post Reach Distribution by Platform",
            color="platform",
            color_discrete_map=self.utils.PLATFORM_COLORS  # Apply platform-specific colors
        )
        st.plotly_chart(fig)

    # New method: Plot bar chart for impressions by platform
    def plot_impressions_by_platform(self):
        impressions_by_platform = self.get_impressions_by_platform()
        fig = px.bar(
            impressions_by_platform,
            x="platform",
            y="total_impressions",
            title="Total Impressions by Platform",
            labels={"total_impressions": "Total Impressions (Views)"},
            color="platform",
            color_discrete_map=self.utils.PLATFORM_COLORS  # Apply platform-specific colors
        )
        st.plotly_chart(fig)

    # New method: Plot horizontal bar chart for top 10 liked posts
    def plot_top_10_liked_posts(self):
        top_10_liked_posts = self.get_top_10_liked_posts()
        fig = px.bar(
            top_10_liked_posts,
            x="likes",
            y="post_id",
            orientation="h",
            labels={"likes": "Likes", "post_id": "Post ID"},
            color="platform",
            color_discrete_map=self.utils.PLATFORM_COLORS  # Apply platform-specific colors
        )
        st.plotly_chart(fig)

    # New method: Plot scatter plot for top 10 shared posts
    def plot_top_10_shared_posts(self):
        top_10_shared_posts = self.get_top_10_shared_posts()
        fig = px.scatter(
            top_10_shared_posts,
            x="post_id",
            y="shares",
            size="shares",
            color="platform",
            hover_data=["platform", "shares"],
            labels={"shares": "Number of Shares", "post_id": "Post ID"},
            color_discrete_map= self.utils.PLATFORM_COLORS  # Apply platform-specific colors
        )
        fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="black")))
        fig.update_layout(xaxis=dict(tickmode="linear"))
        st.plotly_chart(fig)
        



