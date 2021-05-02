# coding: utf-8
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import dash_table
import dash
from flask import request
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import pandas as pd
import time
from src.webApp.global_variables import style_H1, style_H2, style_span, style_b1


def build_page():

    return html.Div(
        [html.P("Profil"),
         ], style={'padding': '20px'})