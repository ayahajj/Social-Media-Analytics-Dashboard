import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import os
import base64

class Utils:
    
    PLATFORM_COLORS = {
        "Facebook": "#4267B2",
        "Instagram": "#E1306C",
        "YouTube": "#FF0000"
    }
        
    def __init__(self, df_posts, df_comments):
        self.df_posts = df_posts
        self.df_comments = df_comments
        
    # Method to dynamically get the icon paths
    def get_base64_icon(self, icon_name):
        """
        Convert a local image file to a base64-encoded string.

        :param icon_name: File name of the icon (e.g., 'likes.svg')
        :return: Base64 encoded string of the image
        """
        icon_path = os.path.join("icons", icon_name)  # Path to local icons folder
        try:
            with open(icon_path, "rb") as img_file:
                return f"data:image/svg+xml;base64,{base64.b64encode(img_file.read()).decode()}"
        except FileNotFoundError:
            return None  # Return None if the file doesn't exist