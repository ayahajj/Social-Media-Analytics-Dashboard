import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

class Utils:
    
    def __init__(self, df):
        self.df = df
        
    # Convert population to text 
    def format_number(self, num):
        if num > 1000000:
            if not num % 1000000:
                return f'{num // 1000000} M'
            return f'{round(num / 1000000, 1)} M'
        return f'{num // 1000} K'

    
    # Calculation year-over-year population migrations
    def calculate_population_difference(self, input_df, input_year):
      selected_year_data = input_df[input_df['year'] == input_year].reset_index()
      previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
      selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
      return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)
