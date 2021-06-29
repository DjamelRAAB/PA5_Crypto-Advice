# coding: utf-8

import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import callback_context
from app import app
from datetime import datetime
from flask import request
import json
import src.webApp.global_variables as gv
import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
import pandas as pd


PATH_LAST_CO = "./src/webApp/assets/dates_records.json"
with open(PATH_LAST_CO, 'w', encoding='utf-8') as track_file:
    json.dump(dict(), track_file)


def build_page():
    df = pd.read_csv("histo_btc.csv") 
    df['time']= pd.to_datetime(df.time,unit='s')

    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(x=df['time'],
                    open=df['addresses_new_non_zero_count'], high=df['addresses_active_count'],
                    low=df['addresses_new_non_zero_count'], close=df['addresses_new_non_zero_count'])
    )
    fig.add_trace(
        go.Scatter(
        x=df['time'],
        y=df['addresses_new_non_zero_count'],
        mode='lines+markers',
        )
    )
                       
    children=([
        html.P(
            "Page d'accueil (pop-up indicant de laisser un feedback"
            "apparaît une fois toutes les 2h, par utilisateur)..."
            "ne fonctionne pas optimalement en mode debug (ecriture fichier local -> refresh)"),
        dbc.Modal([
            dbc.ModalHeader(children="Suivi des usages / FEEDBACK NEEDED !"),
            dbc.ModalBody(children=[
                " Après l'utilisation de l'application, il est possible de renseigner l'usage"
                " dans l'onglet Suivi des usages.\n Merci de laisser également un feedback à"
                " destination de l'Usine en répondant aux questions dans l'onglet Feedback."
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
        dcc.Graph(
        id='example-graph',
        figure=fig
        )
    ])

    app.layout = html.Div(style={'padding': '20px'}, children=children)
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
            user = 'C48679' #request.headers["Oidc-Claim-Sub"]
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
    return app.layout
