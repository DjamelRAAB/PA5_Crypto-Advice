# coding: utf-8
import dash_core_components as dcc
import dash_html_components as html
from app import app
import dash
from global_variables import style_H1, style_H2, style_b1, style_span
from flask import request


def build_page():

    return html.Div([
        item2_feedback()
    ],
        style={'padding': '20px'})


questions = ["Première question ? ",
             "Deuxième question ?",
             "Qu'est-ce qu'on peut améliorer ?"]
choices_answer = ["Très bien", "Bien", "Médiocre"]


def item2_feedback():
    """This function allows to download a DataFrame as ExcelFile

    Returns:
        html.Div
    """
    item = html.Div([
        html.H1("Feedback sur l'application", style=style_H1),
        html.Span("Ce feedback est collecté par Crypto-Advice et sera utilisé "
                  "pour identifier les bonnes pratiques à renforcer ou maintenir",
                  style=style_span),
        html.P('\n'),
        html.H2(questions[0], style=style_H2),
        dcc.Dropdown(
            id='answer_0',
            options=[{'label': name, 'value': name} for name in choices_answer],
            value=None,
            style={'width': '50%'}
        ),
        html.P('\n'),
        html.H2(questions[1], style=style_H2),
        dcc.Dropdown(
            id='answer_1',
            options=[{'label': name, 'value': name} for name in choices_answer],
            value=None,
            style={'width': '50%'}
        ),
        html.P('\n'),
        html.H2(questions[2], style=style_H2),
        dcc.Textarea(
            id='answer_2',
            value='',
            placeholder="Zone de description de l'usage effectué avec l'application",
            style={'width': '100%', 'height': 100},
        ),
        html.Br(),
        html.Button("Envoyer le feedback", id="btn-feedback",
                    n_clicks=0, className="mr-1", style=style_b1),
        html.Div(id="feedback-status")
    ],
        style={'width': '100%', 'display': 'inline-block'}, className="pretty_container"
    )

    @ app.callback(
        dash.dependencies.Output('feedback-status', 'children'),
        [dash.dependencies.Input('btn-feedback', 'n_clicks')],
        [dash.dependencies.State('answer_0', 'value'),
         dash.dependencies.State('answer_1', 'value'),
         dash.dependencies.State('answer_2', 'value')]
    )
    def send_feedback(clicks, answer_0, answer_1, answer_2):
        if clicks == 0:
            return None
        log_feedback = {
            'NNI': request.headers["Oidc-Claim-Sub"],
            questions[0]: answer_0,
            questions[1]: answer_1,
            questions[2]: answer_2}

        print(log_feedback)
        return "Crypto-Advice vous mercie pour votre feedback !"

    return item