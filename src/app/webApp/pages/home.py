# coding: utf-8

import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import callback_context
from dash_html_components.Br import Br
from app import app
from datetime import datetime
from flask import request
import json
import global_variables as gv
import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from sql_request.sql_conector import *
import global_components as gc
import hashlib
import os
import base64
PATH_LAST_CO = "./webApp/assets/dates_records.json"
with open(PATH_LAST_CO, 'w', encoding='utf-8') as track_file:
    json.dump(dict(), track_file)


def build_Footer(height: int=100, width: int=240):

    result = dbc.Container(id='image_acceuil', children=[html.Div([
        html.Img(src=app.get_asset_url('logo.png')),
    ])])
    return result


def build_page():
    logo_path = os.path.join('webApp', 'assets', 'mm3.png')
    contains_login = html.Div([
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
    ])
    children = ([
        dbc.Modal([
            dbc.ModalHeader(children="Suivi des usages / FEEDBACK NEEDED !"),
            dbc.ModalBody(children=[
                " Après l'utilisation de l'application, il est possible de laisser également un feedback à"
                " destination de notre équipe en répondant aux questions dans l'onglet Feedback."
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    children="OK !",
                    id="close-warning-home",
                    className="ml-auto",
                    color="primary"
                )
            )
        ],
            id="warning-home",
            size='lg',
            centered=True,
            is_open=True
        ),
        contains_login,
        html.Br(),
        html.Br(),
        html.Div(id="chose_offer", children=[
            html.Footer(children=[
                    gc.get_image(logo_path, 710, 840),
            ],
                style=gv.FOOTER_STYLE)
        ]),
        html.Br(),
        html.Br(),
        build_Footer(),
    ])


    @ app.callback(
        Output("result_connection", "children"),
        Input("loginButton", "n_clicks"),
        State("usernameBox", "value"),
        State("passwordBox", "value"),
    )
    def log(loginButton, usernameBox, passwordBox):
        if loginButton != 0:
            print(hashlib.sha256(passwordBox.encode()).hexdigest())
            mail, password = get_user(usernameBox)
            print()
            if hashlib.sha256(passwordBox.encode()).hexdigest() == password:
                loginButton = 0
                return "Connection reussie "
            else:
                return "Echec de Connection mail ou mots de passe incorect"
        return None

    @ app.callback(
        Output(component_id="warning-home", component_property="is_open"),
        [Input(component_id="url", component_property="pathname"),
         Input(component_id="close-warning-home", component_property="n_clicks")],
        [State(component_id="warning-home", component_property="is_open")]
    )
    def display_popup_at_first_open_or_close_it(pathname, n_clicks, is_open):
        """
        Handles popup display.
        stores last connexion per user in dates_record.json
        if the last connexion was more than 2 hours ago (or first connexion),
            then pop-up is displayed and last connexion hour is replaced in json
            else no pop-up and no updates

        Args:
            pathname (str) : to launch callback at each visit of accueil
            n_clicks (int) : to close pop-up
            is_open (bool) : to know if pop-up was already on

        Returns:
            new_is_open (bool) : new state of pop-up (displayed or not)
        """
        if pathname == '/' + gv.NAME_APPLICATION + '/':
            dt = datetime.now()
            dt_string = dt.strftime("%d/%m/%Y %H:%M:%S")
            user = request.headers["Host"]
            with open(PATH_LAST_CO, 'r', encoding='utf-8') as track_file:
                last_co = json.load(track_file)
                if user in last_co.keys():
                    last_date = datetime.strptime(last_co[user], "%d/%m/%Y %H:%M:%S")
                    diff = (dt - last_date).seconds // 3600
                    if diff >= 2:
                        new_is_open = True
                        last_co[user] = dt_string
                    else:
                        new_is_open = False
                else:
                    new_is_open = True
                    last_co[user] = dt_string
            with open(PATH_LAST_CO, 'w', encoding='utf-8') as track_file:
                json.dump(last_co, track_file)
        else:
            new_is_open = False

        if callback_context.triggered[0]['prop_id'] != '.':
            ctx = callback_context.triggered[0]['prop_id'].split('.')[0]
            if ctx == 'close-warning-home':
                new_is_open = not is_open

        return new_is_open

    return dbc.Container(id="page", children=children)
