import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import os
from werkzeug.security import check_password_hash
from src.webApp import global_components as gc
from src.webApp import global_variables as gv

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
            ], className='form-group'),
        ]),
    ], className='jumbotron')
])
    return ll



