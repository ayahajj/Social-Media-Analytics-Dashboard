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
        
        print("\n\n", "Facebook PreProcess Start", "\n\n")
        do_facebook_preprocessing()
        print("\n\n", "Facebook PreProcess End", "\n\n")
        print("\n\n", "YouTube PreProcess Start", "\n\n")
        do_youtube_preprocessing()
        print("\n\n", "YouTube PreProcess Start", "\n\n")
        print("\n\n", "Instagram PreProcess Start", "\n\n")
        do_instagram_preprocessing()
        print("\n\n", "Instagram PreProcess Start", "\n\n")
        
        # Save results in Final_Output as social_media_posts.csv
        self.df_post_final.to_csv('../Final_Output/social_media_posts.csv', index=False)
        print("\n\n", "All Values Written to file - PreProcess End", "\n\n")
        

    def do_facebook_preprocessing(self):
        
        if df_post_facebook.empty:
            return
        
        # Remove rows where 'post_origin_text' is empty (i.e., NaN)
        df_post_facebook = df_post_facebook.dropna(subset=['post_origin_text'])

        # Reset the index of the DataFrame after dropping rows, without keeping the old index
        df_post_facebook = df_post_facebook.reset_index(drop=True)

        # Applying the function to the 'post_text' column and creating a new column 'time'
        df['date_difference'] = df['post_origin_text'].apply(extract_facebook_time)

        # Remove empty rows where post_origin_text is empty
        df = df.dropna(subset=['date_difference'])

        # Reset the index after dropping rows
        df = df.reset_index(drop=True)
                
        # Convert the 'date_scraped' column to datetime format
        df_post_facebook['date_scraped'] = pd.to_datetime(df_post_facebook['date_scraped'])
        
        # Apply a custom function to calculate 'date' based on 'date_scraped' for each row
        df_post_facebook['date'] = df_post_facebook.apply(lambda row: get_facebook_post_date(row['date'], row['date_scraped']), axis=1)

        # Fill NaN values in 'likes' column with 0 and then apply a function to parse the values
        df_post_facebook['likes'] = df_post_facebook['likes'].fillna(0)
        df_post_facebook['likes'] = df_post_facebook['likes'].apply(parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'comments' column with 0 and then apply a function to parse the values
        df_post_facebook['comments'] = df_post_facebook['comments'].fillna(0)
        df_post_facebook['comments'] = df_post_facebook['comments'].apply(parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'shares' column with 0 and then apply a function to parse the values
        df_post_facebook['shares'] = df_post_facebook['shares'].fillna(0)
        df_post_facebook['shares'] = df_post_facebook['shares'].apply(parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'views' column with 0 and then apply a function to parse the values
        df_post_facebook['views'] = df_post_facebook['views'].fillna(0)
        df_post_facebook['views'] = df_post_facebook['views'].apply(parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'followers' column with 0 and then apply a function to parse the values
        df_post_facebook['followers'] = df_post_facebook['followers'].fillna(0)
        df_post_facebook['followers'] = df_post_facebook['followers'].apply(parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'country' column with an empty string
        df_post_facebook['country'] = df_post_facebook['country'].fillna("")
        
         # Append the processed Facebook data to the global DataFrame (self.df_post_final) that holds posts from all platforms
        self.df_post_final = pd.concat(
            [self.df_post_final, 
            df_post_facebook[
                ['user_id', 'platform', 'post_id', 'date', 
                 'likes', 'comments', 'shares', 'post_text', 
                 'post_origin_text', 'date_scraped', 'views', 
                 'followers', 'country', 'content_type', 
                 'sentiment_score']
                 ]
            ], ignore_index=True)


    # Function to extract time (e.g., '6h')
    def extract_facebook_time(post_text):
        # Matching time formats like '6h', '5d', '2m', '1y'
        match = re.search(r'(\d+)(h|d|m|y)', post_text)
        return match.group(0) if match else None


    # Function to calculate post date
    def get_facebook_post_date(relative_time, scrape_date):
        match = re.match(r"(\d+)(m|h|d|y)", relative_time)
        if match:
            value, unit = int(match.group(1)), match.group(2)
            if unit == "m":
                return scrape_date - timedelta(minutes=value)
            elif unit == "h":
                return scrape_date - timedelta(hours=value)
            elif unit == "f":
                return scrape_date - timedelta(days=value)
            elif unit == "y":
                return scrape_date.replace(year=scrape_date.year - value)

        return None


    # Function to convert likes count to integer
    def parse_facebook_likes_comments_shares_views_followers(values):
        values = str(values).replace(" ", "")  # Remove all spaces
        match = re.match(r"(\d+(\.\d+)?)([KM]?)", values)
        if match:
            value, suffix = float(match.group(1)), match.group(3)
            if suffix == "K":
                return int(value * 1_000)
            elif suffix == "M":
                return int(value * 1_000_000)
            return int(value)
        return 0
 
 
    def do_youtube_preprocessing(self):
        
        if df_post_youtube.empty:
            return
        
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
        df_post_youtube['likes'] = df_post_youtube['likes'].apply(parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'comments' column with 0 and then apply a function to parse the values
        df_post_youtube['comments'] = df_post_youtube['comments'].fillna(0)
        df_post_youtube['comments'] = df_post_youtube['comments'].apply(parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'shares' column with 0 and then apply a function to parse the values
        df_post_youtube['shares'] = df_post_youtube['shares'].fillna(0)
        df_post_youtube['shares'] = df_post_youtube['shares'].apply(parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'views' column with 0 and then apply a function to parse the values
        df_post_youtube['views'] = df_post_youtube['views'].fillna(0)
        df_post_youtube['views'] = df_post_youtube['views'].apply(parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'followers' column with 0 and then apply a function to parse the values
        df_post_youtube['followers'] = df_post_youtube['followers'].fillna(0)
        df_post_youtube['followers'] = df_post_youtube['followers'].apply(parse_youtube_likes_comments_shares_views_followers)

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
    def parse_youtube_likes_comments_shares_views_followers(values):
        values = str(values).replace(" ", "")  # Remove all spaces
        match = re.match(r"(\d+(\.\d+)?)([KM]?)", values)
        if match:
            value, suffix = float(match.group(1)), match.group(3)
            if suffix == "K":
                return int(value * 1_000)
            elif suffix == "M":
                return int(value * 1_000_000)
            return int(value)
        return 0
 

    def do_instagram_preprocessing(self):
        
        if df_post_instagram.empty:
            return
        
        # Remove rows where 'post_origin_text' is empty (i.e., NaN)
        df_post_instagram = df_post_instagram.dropna(subset=['post_origin_text'])

        # Reset the index of the DataFrame after dropping rows, without keeping the old index
        df_post_instagram = df_post_instagram.reset_index(drop=True)
                
        # Convert the 'date_scraped' column to datetime format
        df_post_instagram['date_scraped'] = pd.to_datetime(df_post_instagram['date_scraped'])
        
        # Apply a custom function to calculate 'date' based on 'date_scraped' for each row
        df_post_instagram['date'] = df_post_instagram.apply(lambda row: get_instagram_post_date(row['date'], row['date_scraped']), axis=1)

        # Fill NaN values in 'likes' column with 0 and then apply a function to parse the values
        df_post_instagram['likes'] = df_post_instagram['likes'].fillna(0)
        df_post_instagram['likes'] = df_post_instagram['likes'].apply(parse_instagram_likes)

        # Fill NaN values in 'comments' column with 0 and then apply a function to parse the values
        df_post_instagram['comments'] = df_post_instagram['comments'].fillna(0)
        df_post_instagram['comments'] = df_post_instagram['comments'].apply(parse_instagram_likes)

        # Fill NaN values in 'shares' column with 0 and then apply a function to parse the values
        df_post_instagram['shares'] = df_post_instagram['shares'].fillna(0)
        df_post_instagram['shares'] = df_post_instagram['shares'].apply(parse_instagram_likes)

        # Fill NaN values in 'views' column with 0 and then apply a function to parse the values
        df_post_instagram['views'] = df_post_instagram['views'].fillna(0)
        df_post_instagram['views'] = df_post_instagram['views'].apply(parse_instagram_likes)

        # Fill NaN values in 'followers' column with 0 and then apply a function to parse the values
        df_post_instagram['followers'] = df_post_instagram['followers'].fillna(0)
        df_post_instagram['followers'] = df_post_instagram['followers'].apply(parse_instagram_likes)

        # Fill NaN values in 'country' column with an empty string
        df_post_instagram['country'] = df_post_instagram['country'].fillna("")
        
         # Append the processed YouTube data to the global DataFrame (self.df_post_final) that holds posts from all platforms
        self.df_post_final = pd.concat(
            [self.df_post_final, 
            df_post_instagram[
                ['user_id', 'platform', 'post_id', 'date', 
                 'likes', 'comments', 'shares', 'post_text', 
                 'post_origin_text', 'date_scraped', 'views', 
                 'followers', 'country', 'content_type', 
                 'sentiment_score']
                 ]
            ], ignore_index=True)


    # Function to extract the number of likes as integers
    def parse_instagram_likes(likes):
        # Remove commas and extract only the digits
        return int(re.sub(r'[^\d]', '', likes))


    # Function to calculate post date
    def get_instagram_post_date(relative_time, scrape_date):
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
       






