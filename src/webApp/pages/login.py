import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import os
from src.webApp import global_components as gc
from src.webApp import global_variables as gv
from app import app
import sys
from src.sql_request.sql_conector import *


def build_page():
    logo_path = os.path.join('src', 'webApp', 'images', 'crypto_advice.png')
    ll = dbc.Container([
        html.Br(),
        dbc.Container([
            dcc.Location(id='urlLogin', refresh=True),
            html.Div([
                dbc.Container(
                    html.Footer(children=[gc.get_image(logo_path, 200, 600)],style=gv.FOOTER_STYLE),
                    ),
                dbc.Container(id='loginType', children=[
                    dcc.Input(
                        placeholder='Enter your username',
                        type='text',
                        id='usernameBox',
                        className='form-control',
                        n_submit=0,
                    ),
                    html.Br(),
                    dcc.Input(
                        placeholder='Enter your password',
                        type='password',
                        id='passwordBox',
                        className='form-control',
                        n_submit=0,
                    ),
                    html.Br(),
                    html.Button(
                        children='Login',
                        n_clicks=0,
                        type='submit',
                        id='loginButton',
                        className='btn btn-primary btn-lg'
                    ),
                    html.Br(),
                    html.Div(id="number-out"),
                ], className='form-group'),
            ]),
        ], className='jumbotron')])    

    @ app.callback(
        Output("number-out", "children"),
        Input("loginButton","n_clicks"),
        State("usernameBox", "value"),
        State("passwordBox", "value"),
    )
    def number_render(loginButton,usernameBox, passwordBox):
        print(loginButton,usernameBox, passwordBox)
        add_user("loginButton","usernameBox","email","password","2020-02-01","1")
        return " connection sucise "

    return ll



