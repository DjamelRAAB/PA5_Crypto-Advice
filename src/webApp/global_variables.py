# coding: utf-8

"""

global_variables
*****************

This script defines global variables used in the web application.

"""

import dash_bootstrap_components as dbc

import socket


# ## Layout variables ###
########################

APP_THEME = dbc.themes.LUX

style_span = {'color': '#0a84ff', 'font-style': 'italic', 'font-size': '1rem'}
style_H1 = {'color': 'black', 'font-style': 'italic', 'font-weight': 'bold', 'font-size': '1.5rem'}
style_H2 = {'color': 'black', 'font-size': '1.1rem'}
style_b1 = {'background-color': '#0a84ff', 'color': 'white', 'font-weight': 900}
style_b2 = {'background-color': 'red', 'color': '#0a84ff', 'font-weight': 1500}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    'overflowY': 'auto'
}

FOOTER_STYLE = {
    # "display": "flex",
    "justify-content": "center",
    "vertical-align": "bottom",
    "bottom": 0,
    'backgroundColor': '#000000 '   
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# APP_TITLE = 'CRYPTO ADVICE'

DEFAULT_LAYOUT = {}


#

NAME_APPLICATION =  'crypto-advice' 
# if socket.gethostname() == "dceyy21e":
#     NAME_APPLICATION = "dash-template"
# else:
#     NAME_APPLICATION = "dash-template-hp"

USER_GUID_PATH = "assets/Guide d'emploi.pdf"