# coding: utf-8

import dash_html_components as html
from global_variables import USER_GUID_PATH

def build_page():
    return html.Div(
        [html.Iframe(src= USER_GUID_PATH,
                     style={"width": "800px", "height": "600px"})
         ], style={'padding': '20px'})
