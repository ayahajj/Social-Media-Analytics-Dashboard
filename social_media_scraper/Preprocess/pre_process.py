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
import time
from datetime import datetime, timedelta
import re

class PreProcess:
    def __init__(self):
        self.df_post_final = pd.DataFrame(columns=[
            "user_id", 
            "platform", 
            "post_id", 
            "date", 
            "likes", 
            "comments", 
            "shares", 
            "post_text", 
            "post_origin_text", 
            "date_scraped", 
            "views", 
            "followers", 
            "country", 
            "content_type", 
            "sentiment_score"
        ])
        
        self.df_post_facebook = pd.read_excel('../Scraping_Output/facebook_data.xlsx')
        self.df_post_youtube = pd.read_excel('.//Scraping_Output/youtube_data.xlsx')
        self.df_post_instagram = pd.read_excel('../Scraping_Output/instagram_data.xlsx')

    def do_preprocessing(self):
        do_facebook_preprocessing()
        do_youtube_preprocessing()
        do_instagram_preprocessing()
        
        # Save results in Final_Output as social_media_posts.csv
        self.df_post_final.to_csv('../Final_Output/social_media_posts.csv', index=False)

    def do_facebook_preprocessing(self):
        return True

    def do_youtube_preprocessing(self):
        
        # Remove rows where 'post_origin_text' is empty (i.e., NaN)
        df_post_youtube = df_post_youtube.dropna(subset=['post_origin_text'])

        # Reset the index of the DataFrame after dropping rows, without keeping the old index
        df_post_youtube = df_post_youtube.reset_index(drop=True)
                
        # Convert the 'date_scraped' column to datetime format
        df_post_youtube['date_scraped'] = pd.to_datetime(df_post_youtube['date_scraped'])
        
        # Apply a custom function to calculate 'date' based on 'date_scraped' for each row
        df_post_youtube['date'] = df_post_youtube.apply(lambda row: get_youtube_post_date(row['date'], row['date_scraped']), axis=1)

        # Fill NaN values in 'likes' column with 0 and then apply a function to parse the values
        df_post_youtube['likes'] = df_post_youtube['likes'].fillna(0)
        df_post_youtube['likes'] = df_post_youtube['likes'].apply(parse_likes_comments_shares_views_followers)

        # Fill NaN values in 'comments' column with 0 and then apply a function to parse the values
        df_post_youtube['comments'] = df_post_youtube['comments'].fillna(0)
        df_post_youtube['comments'] = df_post_youtube['comments'].apply(parse_likes_comments_shares_views_followers)

        # Fill NaN values in 'shares' column with 0 and then apply a function to parse the values
        df_post_youtube['shares'] = df_post_youtube['shares'].fillna(0)
        df_post_youtube['shares'] = df_post_youtube['shares'].apply(parse_likes_comments_shares_views_followers)

        # Fill NaN values in 'views' column with 0 and then apply a function to parse the values
        df_post_youtube['views'] = df_post_youtube['views'].fillna(0)
        df_post_youtube['views'] = df_post_youtube['views'].apply(parse_likes_comments_shares_views_followers)

        # Fill NaN values in 'followers' column with 0 and then apply a function to parse the values
        df_post_youtube['followers'] = df_post_youtube['followers'].fillna(0)
        df_post_youtube['followers'] = df_post_youtube['followers'].apply(parse_likes_comments_shares_views_followers)

        # Fill NaN values in 'country' column with an empty string
        df_post_youtube['country'] = df_post_youtube['country'].fillna("")
        
         # Append the processed YouTube data to the global DataFrame (self.df_post_final) that holds posts from all platforms
        self.df_post_final = pd.concat(
            [self.df_post_final, 
            df_post_youtube[
                ['user_id', 'platform', 'post_id', 'date', 
                 'likes', 'comments', 'shares', 'post_text', 
                 'post_origin_text', 'date_scraped', 'views', 
                 'followers', 'country', 'content_type', 
                 'sentiment_score']
                 ]
            ], ignore_index=True)



    def do_instagram_preprocessing(self):
        return True


    
    # Function to calculate post date
    def get_youtube_post_date(relative_time, scrape_date):
        match = re.match(r"(\d+) (minute|hour|day|year)s? ago", relative_time)
        if match:
            value, unit = int(match.group(1)), match.group(2)
            if unit == "minute":
                return scrape_date - timedelta(minutes=value)
            elif unit == "hour":
                return scrape_date - timedelta(hours=value)
            elif unit == "day":
                return scrape_date - timedelta(days=value)
            elif unit == "year":
                return scrape_date.replace(year=scrape_date.year - value)
        elif "edited" in relative_time:
            return get_post_date(relative_time.replace(" (edited)", ""))
        return None
       
     
    # Function to convert likes count to integer
    def parse_likes_comments_shares_views_followers(values):
        values = str(values)  # Ensure values is a string
        match = re.match(r"(\d+(\.\d+)?)([KM]?)", values)
        if match:
            value, suffix = float(match.group(1)), match.group(3)
            if suffix == "K":
                return int(value * 1_000)
            elif suffix == "M":
                return int(value * 1_000_000)
            return int(value)
        return 0
        

