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
import os
import traceback
import nltk
import string
from nltk.corpus import stopwords
from textblob import TextBlob
from langdetect import detect, DetectorFactory
nltk.download("stopwords")

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
                
        self.df_post_facebook = pd.read_excel(r'social_media_scraper\Scraping_Output\facebook_data.xlsx')
        self.df_post_youtube = pd.read_excel(r'social_media_scraper\Scraping_Output\youtube_data.xlsx')
        self.df_post_instagram = pd.read_excel(r'social_media_scraper\Scraping_Output\instagram_data.xlsx')

        # Ensure consistent language detection results
        DetectorFactory.seed = 0  

        # Download stopwords if not already downloaded
        nltk.download("stopwords")
        self.stop_words = set(stopwords.words("english"))


    def do_preprocessing(self):
        
        try:
            print("\n\n", "Facebook PreProcess Start", "\n\n")
            self.do_facebook_preprocessing()
            print("\n\n", "Facebook PreProcess End", "\n\n")
        except Exception as e:
            print("\n\n", "Error during Facebook PreProcessing:", str(e), "\n\n")
            traceback.print_exc()  # Prints the full traceback
            return
        
        try:
            print("\n\n", "YouTube PreProcess Start", "\n\n")
            self.do_youtube_preprocessing()
            print("\n\n", "YouTube PreProcess End", "\n\n")
        except Exception as e:
            print("\n\n", "Error during YouTube PreProcessing:", str(e), "\n\n")
            traceback.print_exc()  # Prints the full traceback
            return
        
        try:
            print("\n\n", "Instagram PreProcess Start", "\n\n")
            self.do_instagram_preprocessing()
            print("\n\n", "Instagram PreProcess End", "\n\n")
        except Exception as e:
            print("\n\n", "Error during Instagram PreProcessing:", str(e), "\n\n")
            traceback.print_exc()  # Prints the full traceback
            return
            
        try:
            self.df_post_final['user_id'] = self.df_post_final['user_id'].iloc[0]
            print("\n\n", "UserID set", "\n\n")
        except Exception as e:
            print("\n\n", "Error setting user_id:", str(e), "\n\n")
            traceback.print_exc()  # Prints the full traceback
            return
        
        try:
            # Apply language detection and sentiment analysis
            self.df_post_final["post_language"] = self.df_post_final["post_text"].apply(self.detect_language)
            self.df_post_final["sentiment_score"] = self.df_post_final.apply(lambda row: self.analyze_sentiment(row["post_text"]) if row["post_language"] in ["en", "ar"] else None, axis=1)

            print("\n\n", "Sentiment Score set", "\n\n")
        except Exception as e:
            print("\n\n", "Error Sentiment Score:", str(e), "\n\n")
            traceback.print_exc()  # Prints the full traceback
            return
        
        try:
            # Save results in Final_Output as social_media_posts.xlsx
            self.df_post_final.to_excel(r'social_media_scraper/Final_Output/social_media_posts.xlsx', index=False)
            print("\n\n", "All Values Written to file - PreProcess End", "\n\n")
        except Exception as e:
            print("\n\n", "Error writing to file:", str(e), "\n\n")
            traceback.print_exc()  # Prints the full traceback
            return

        print("\n\n", "All Values Written to file - PreProcess End", "\n\n")
        

    def do_facebook_preprocessing(self):
        
        if self.df_post_facebook.empty:
            return
        
        # Remove rows where 'post_origin_text' is empty (i.e., NaN)
        self.df_post_facebook = self.df_post_facebook.dropna(subset=['post_origin_text'])

        # Reset the index of the DataFrame after dropping rows, without keeping the old index
        self.df_post_facebook = self.df_post_facebook.reset_index(drop=True)

        # Applying the function to the 'post_text' column and creating a new column 'time'
        self.df_post_facebook['date_difference'] = self.df_post_facebook['post_origin_text'].apply(self.extract_facebook_time)

        # Remove empty rows where post_origin_text is empty
        self.df_post_facebook = self.df_post_facebook.dropna(subset=['date_difference'])

        # Reset the index after dropping rows
        self.df_post_facebook = self.df_post_facebook.reset_index(drop=True)
                
        # Convert the 'date_scraped' column to datetime format
        self.df_post_facebook['date_scraped'] = pd.to_datetime(self.df_post_facebook['date_scraped'])
        
        # Apply a custom function to calculate 'date' based on 'date_scraped' for each row
        self.df_post_facebook['date'] = self.df_post_facebook.apply(lambda row: self.get_facebook_post_date(row['date_difference'], row['date_scraped']), axis=1)

        # Fill NaN values in 'likes' column with 0 and then apply a function to parse the values
        self.df_post_facebook['likes'] = self.df_post_facebook['likes'].fillna(0)
        self.df_post_facebook['likes'] = self.df_post_facebook['likes'].apply(self.parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'comments' column with 0 and then apply a function to parse the values
        self.df_post_facebook['comments'] = self.df_post_facebook['comments'].fillna(0)
        self.df_post_facebook['comments'] = self.df_post_facebook['comments'].apply(self.parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'shares' column with 0 and then apply a function to parse the values
        self.df_post_facebook['shares'] = self.df_post_facebook['shares'].fillna(0)
        self.df_post_facebook['shares'] = self.df_post_facebook['shares'].apply(self.parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'views' column with 0 and then apply a function to parse the values
        self.df_post_facebook['views'] = self.df_post_facebook['views'].fillna(0)
        self.df_post_facebook['views'] = self.df_post_facebook['views'].apply(self.parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'followers' column with 0 and then apply a function to parse the values
        self.df_post_facebook['followers'] = self.df_post_facebook['followers'].fillna(0)
        self.df_post_facebook['followers'] = self.df_post_facebook['followers'].apply(self.parse_facebook_likes_comments_shares_views_followers)

        # Fill NaN values in 'country' column with an empty string
        self.df_post_facebook['country'] = self.df_post_facebook['country'].fillna("")
        
         # Append the processed Facebook data to the global DataFrame (self.df_post_final) that holds posts from all platforms
        self.df_post_final = pd.concat(
            [self.df_post_final, 
            self.df_post_facebook[
                ['user_id', 'platform', 'post_id', 'date', 
                 'likes', 'comments', 'shares', 'post_text', 
                 'post_origin_text', 'date_scraped', 'views', 
                 'followers', 'country', 'content_type', 
                 'sentiment_score']
                 ]
            ], ignore_index=True)


    # Function to extract time (e.g., '6h')
    def extract_facebook_time(self,post_text):
        # Matching time formats like '6h', '5d', '2m', '1y'
        match = re.search(r'(\d+)(h|d|m|y)', post_text)
        return match.group(0) if match else None


    # Function to calculate post date
    def get_facebook_post_date(self,relative_time, scrape_date):
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
    def parse_facebook_likes_comments_shares_views_followers(self,values):
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
        
        if self.df_post_youtube.empty:
            return
        
        # Remove rows where 'post_origin_text' is empty (i.e., NaN)
        self.df_post_youtube = self.df_post_youtube.dropna(subset=['post_origin_text'])

        # Reset the index of the DataFrame after dropping rows, without keeping the old index
        self.df_post_youtube = self.df_post_youtube.reset_index(drop=True)
                
        # Convert the 'date_scraped' column to datetime format
        self.df_post_youtube['date_scraped'] = pd.to_datetime(self.df_post_youtube['date_scraped'])
        
        # Remove empty rows where date is empty
        self.df_post_youtube = self.df_post_youtube.dropna(subset=['date'])

        # Apply a custom function to calculate 'date' based on 'date_scraped' for each row
        self.df_post_youtube['date'] = self.df_post_youtube.apply(lambda row: self.get_youtube_post_date(row['date'], row['date_scraped']), axis=1)

        # Fill NaN values in 'likes' column with 0 and then apply a function to parse the values
        self.df_post_youtube['likes'] = self.df_post_youtube['likes'].fillna(0)
        self.df_post_youtube['likes'] = self.df_post_youtube['likes'].apply(self.parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'comments' column with 0 and then apply a function to parse the values
        self.df_post_youtube['comments'] = self.df_post_youtube['comments'].fillna(0)
        self.df_post_youtube['comments'] = self.df_post_youtube['comments'].apply(self.parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'shares' column with 0 and then apply a function to parse the values
        self.df_post_youtube['shares'] = self.df_post_youtube['shares'].fillna(0)
        self.df_post_youtube['shares'] = self.df_post_youtube['shares'].apply(self.parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'views' column with 0 and then apply a function to parse the values
        self.df_post_youtube['views'] = self.df_post_youtube['views'].fillna(0)
        self.df_post_youtube['views'] = self.df_post_youtube['views'].apply(self.parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'followers' column with 0 and then apply a function to parse the values
        self.df_post_youtube['followers'] = self.df_post_youtube['followers'].fillna(0)
        self.df_post_youtube['followers'] = self.df_post_youtube['followers'].apply(self.parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'country' column with an empty string
        self.df_post_youtube['country'] = self.df_post_youtube['country'].fillna("")
        
         # Append the processed YouTube data to the global DataFrame (self.df_post_final) that holds posts from all platforms
        self.df_post_final = pd.concat(
            [self.df_post_final, 
            self.df_post_youtube[
                ['user_id', 'platform', 'post_id', 'date', 
                 'likes', 'comments', 'shares', 'post_text', 
                 'post_origin_text', 'date_scraped', 'views', 
                 'followers', 'country', 'content_type', 
                 'sentiment_score']
                 ]
            ], ignore_index=True)


    # Function to calculate post date
    def get_youtube_post_date(self,relative_time, scrape_date):
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
    def parse_youtube_likes_comments_shares_views_followers(self,values):
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
        
        if self.df_post_instagram.empty:
            return
        
        # Remove rows where 'post_origin_text' is empty (i.e., NaN)
        self.df_post_instagram = self.df_post_instagram.dropna(subset=['post_origin_text'])

        # Reset the index of the DataFrame after dropping rows, without keeping the old index
        self.df_post_instagram = self.df_post_instagram.reset_index(drop=True)
                
        # Convert the 'date_scraped' column to datetime format
        self.df_post_instagram['date_scraped'] = pd.to_datetime(self.df_post_instagram['date_scraped'])
        
        # Remove empty rows where date is empty
        self.df_post_instagram = self.df_post_instagram.dropna(subset=['date'])
        
        # Apply a custom function to calculate 'date' based on 'date_scraped' for each row
        self.df_post_instagram['date'] = self.df_post_instagram.apply(lambda row: self.get_instagram_post_date(row['date'], row['date_scraped']), axis=1)

        # Fill NaN values in 'likes' column with 0 and then apply a function to parse the values
        self.df_post_instagram['likes'] = self.df_post_instagram['likes'].fillna(0)
        self.df_post_instagram['likes'] = self.df_post_instagram['likes'].apply(self.parse_instagram_likes)

        # Fill NaN values in 'comments' column with 0 and then apply a function to parse the values
        self.df_post_instagram['comments'] = self.df_post_instagram['comments'].fillna(0)
        # self.df_post_instagram['comments'] = self.df_post_instagram['comments'].apply(self.parse_instagram_likes)

        # Fill NaN values in 'shares' column with 0 and then apply a function to parse the values
        self.df_post_instagram['shares'] = self.df_post_instagram['shares'].fillna(0)
        # self.df_post_instagram['shares'] = self.df_post_instagram['shares'].apply(self.parse_instagram_likes)

        # Fill NaN values in 'views' column with 0 and then apply a function to parse the values
        self.df_post_instagram['views'] = self.df_post_instagram['views'].fillna(0)
        # self.df_post_instagram['views'] = self.df_post_instagram['views'].apply(self.parse_instagram_likes)

        # Fill NaN values in 'followers' column with 0 and then apply a function to parse the values
        self.df_post_instagram['followers'] = self.df_post_instagram['followers'].fillna(0)
        self.df_post_instagram['followers'] = self.df_post_instagram['followers'].apply(self.parse_youtube_likes_comments_shares_views_followers)

        # Fill NaN values in 'country' column with an empty string
        self.df_post_instagram['country'] = self.df_post_instagram['country'].fillna("")
        
         # Append the processed YouTube data to the global DataFrame (self.df_post_final) that holds posts from all platforms
        self.df_post_final = pd.concat(
            [self.df_post_final, 
            self.df_post_instagram[
                ['user_id', 'platform', 'post_id', 'date', 
                 'likes', 'comments', 'shares', 'post_text', 
                 'post_origin_text', 'date_scraped', 'views', 
                 'followers', 'country', 'content_type', 
                 'sentiment_score']
                 ]
            ], ignore_index=True)


    # Function to extract the number of likes as integers
    def parse_instagram_likes(self,likes):
        # Remove commas and extract only the digits
        return int(re.sub(r'[^\d]', '', likes))


    # Function to calculate post date
    def get_instagram_post_date(self, relative_time, scrape_date):
        return datetime.strptime(relative_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # match = re.match(r"(\d+) (minute|hour|day|year)s? ago", relative_time)
        # if match:
        #     value, unit = int(match.group(1)), match.group(2)
        #     if unit == "minute":
        #         return scrape_date - timedelta(minutes=value)
        #     elif unit == "hour":
        #         return scrape_date - timedelta(hours=value)
        #     elif unit == "day":
        #         return scrape_date - timedelta(days=value)
        #     elif unit == "year":
        #         return scrape_date.replace(year=scrape_date.year - value)
        # elif "edited" in relative_time:
        #     return get_post_date(relative_time.replace(" (edited)", ""))
        # return None


    def detect_language(self, text):
        """Detect the language using langdetect."""
        try:
            return detect(text)  # Returns language code (e.g., 'en', 'fr', 'es')
        except:
            return None  # Return None if detection fails


    def preprocess_text(self, text):
        """Clean and tokenize the text"""
        # Check if the text is a string
        if not isinstance(text, str):
            return ""
        
        # Remove punctuation and convert to lowercase
        text = text.lower().translate(str.maketrans("", "", string.punctuation))

        # Tokenization and remove stopwords
        words = text.split()
        words = [word for word in words if word not in self.stop_words]

        return " ".join(words)


    def analyze_sentiment(self,text):
        """Perform Sentiment Analysis using the textblob library
        Return sentiment polarity (-1 to 1) only if the text is in English."""
        print("Languge :", str(self.detect_language(text)))
        
        if self.detect_language(text) == "en":  # Only analyze if text is in English
            processed_text = self.preprocess_text(text)
            return TextBlob(processed_text).sentiment.polarity
            
        if self.detect_language(text) == "ar":  # Only analyze if text is in Arabic
            processed_text = self.preprocess_text(text)
            return TextBlob(processed_text).sentiment.polarity
            
        return None  # Return None for non-English texts


