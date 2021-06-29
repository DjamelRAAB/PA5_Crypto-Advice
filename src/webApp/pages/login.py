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
import hashlib
import flask

def build_page():
    logo_path = os.path.join('src', 'webApp', 'images', 'crypto_advice.png')
    login_page = dbc.Container(id= "page", children =[
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
                        className='btn btn-success  '
                    ),
                    html.Button(
                        children='subscrib',
                        n_clicks=0,
                        type='submit',
                        id='subscrib',
                        className='btn btn-primary '
                    ),
                    html.Br(),
                    html.Div(id="result_connection"),
                ], className='form-group'),
            ]),
        ], className='jumbotron')])    

    # @ app.callback(
    #     Output("page", "children"),
    #     Input("loginButton","n_clicks"),
    #     Input("subscrib","n_clicks"),
    #     State("usernameBox", "value"),
    #     State("passwordBox", "value"),
    # )
    # def sub(subscrib,loginButton,usernameBox, passwordBox):
    #     if (subscrib == 1):
    #         suscrybe_page = dbc.Container([
    #             html.Br(),
    #             dbc.Container([
                    
    #                 html.Div([
    #                     dbc.Container(
    #                         html.Footer(children=[gc.get_image(logo_path, 200, 600)],style=gv.FOOTER_STYLE),
    #                         ),
    #                     dbc.Container(id='loginType', children=[
    #                         dcc.Input(
    #                             placeholder='Enter your username',
    #                             type='text',
    #                             id='usernameBox',
    #                             className='form-control',
    #                             n_submit=0,
    #                         ),
    #                         html.Br(),
    #                         dcc.Input(
    #                             placeholder='Enter your username',
    #                             type='text',
    #                             id='usernameBox',
    #                             className='form-control',
    #                             n_submit=0,
    #                         ),
    #                         html.Br(),
    #                         dcc.Input(
    #                             placeholder='Enter your username',
    #                             type='text',
    #                             id='usernameBox',
    #                             className='form-control',
    #                             n_submit=0,
    #                         ),
    #                         html.Br(),
    #                         dcc.Input(
    #                             placeholder='Enter your username',
    #                             type='text',
    #                             id='usernameBox',
    #                             className='form-control',
    #                             n_submit=0,
    #                         ),
    #                         html.Br(),
    #                         dcc.Input(
    #                             placeholder='Enter your password',
    #                             type='password',
    #                             id='passwordBox',
    #                             className='form-control',
    #                             n_submit=0,
    #                         ),
    #                         html.Br(),
    #                         html.Button(
    #                             children='Login',
    #                             n_clicks=0,
    #                             type='submit',
    #                             id='loginButton',
    #                             className='btn btn-success  '
    #                         ),
    #                         html.Br(),
    #                         html.Div(id="number-out"),
    #                     ], className='form-group'),
    #                 ]),
    #             ], className='jumbotron')]) 
    #         return suscrybe_page


    @ app.callback(
        Output("result_connection", "children"),
        Input("loginButton","n_clicks"),
        State("usernameBox", "value"),
        State("passwordBox", "value"),
    )
    def log(loginButton,usernameBox, passwordBox):
        if loginButton == 1 :
            print(hashlib.sha256(passwordBox.encode()).hexdigest())
            mail, password = get_user(usernameBox)
            if hashlib.sha256(passwordBox.encode()).hexdigest() == password :
                loginButton = 0
                return "Connection reussie "
            else :
                return "Echec de Connection mail ou mots de passe incorect"
        return None

    return login_page 



