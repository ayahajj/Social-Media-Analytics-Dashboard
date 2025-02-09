import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

class IndicatorsGenerator:
    
    def __init__(self, df):
        self.df = df
        
    # Heatmap
    def make_heatmap(self, input_df, input_y, input_x, input_color, input_color_theme):
        heatmap = alt.Chart(input_df).mark_rect().encode(
                y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
                x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
                color=alt.Color(f'max({input_color}):Q',
                                 legend=None,
                                 scale=alt.Scale(scheme=input_color_theme)),
                stroke=alt.value('black'),
                strokeWidth=alt.value(0.25),
            ).properties(width=900
            ).configure_axis(
            labelFontSize=12,
            titleFontSize=12
            ) 
        # height=300
        return heatmap


    # Choropleth map
    def make_choropleth(self, input_df, input_id, input_column, input_color_theme, df_selected_year):
        choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                                   color_continuous_scale=input_color_theme,
                                   range_color=(0, max(df_selected_year.population)),
                                   scope="usa",
                                   labels={'population':'Population'}
                                  )
        choropleth.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        return choropleth
