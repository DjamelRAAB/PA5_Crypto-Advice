# coding: utf-8

"""

page_retriever
***************

This script controls the web pages available in the app and their URL.
This script is used to build and provide the whole content of a page (logo, side bar menu, main content...)
to index.py

"""

import os
import base64

import dash_bootstrap_components as dbc
import dash_html_components as html
from src.webApp.pages import home, profil, news, userguide, trade, feedBack
from src.webApp import global_variables as gv
from src.webApp import global_components as gc


APP_PAGES = {
    'home': {
        'Label': 'Accueil',
        'URL': '/' + gv.NAME_APPLICATION + '/',
        'Content': home.build_page()},
    'page1_TrainPrediction': {
        'Label': 'Profil ',
        'URL': '/' + gv.NAME_APPLICATION + '/profil',
        'Content': profil.build_page()},
    'page2': {
        'Label': 'Trade',
        'URL': '/' + gv.NAME_APPLICATION + '/trade',
        'Content': trade.build_page()},
    "Reporting": {
        'Label': "News",
        'URL': '/' + gv.NAME_APPLICATION + '/news',
        'Content': news.build_page()},
    "Feedback": {
        'Label': "Feedback",
        'URL': '/' + gv.NAME_APPLICATION + '/feedback',
        'Content': feedBack.build_page()},
    "userguide": {
        'Label': "User guide",
        'URL': '/' + gv.NAME_APPLICATION + '/userguide',
        'Content': userguide.build_page()}
}
""" APP_PAGES dictionnary get the list of all pages available in the web application.
Each key contains a sub-dictionnay with 3 values :
    - Label : label used to build the menu in the side bar
    - URL : URL to reach the page
    - Content : function to call to get the page content
"""
PAGES_URLS = [APP_PAGES[page]['URL'] for page in APP_PAGES]


def build_page_not_found(height: int = 1000, width: int = 1000):
    image_path = os.path.join('src', 'webApp', 'images', 'page_not_found.jpg')
    image_encoded = base64.b64encode(open(image_path, 'rb').read())

    not_found = html.Img(src='data:image/png;base64,{}'.format(image_encoded.decode()),
                         height='75%', width='75%')

    return not_found


def get_page_menu():
    pages = []
    for page_id in APP_PAGES:

        page_label = APP_PAGES[page_id]['Label']
        page_url = APP_PAGES[page_id]['URL']

        if page_url is None:
            # In this case we have a header instead of a link page
            pages.append(dbc.NavLink(page_label))
        else:
            pages.append(dbc.NavLink(page_label, href=page_url, id=page_id))

    return pages


def build_Footer(height: int=100, width: int=240):
    logo_path = os.path.join('src', 'webApp', 'images', 'crypto_advice.png')

    footer = html.Footer(children=[
        gc.get_image(logo_path, height, width),
    ],
        style=gv.FOOTER_STYLE)

    return footer


def build_contact_section(coords):
    """This function creates and html.Ul component

    Args:
        coords - list of dicts [{'name':, 'email':, 'desc':}, ...]
    Returns:
        html.Ul
    """
    html_coords = []
    for i in coords:
        html_coords.append(html.Li(
            [
                html.A(
                    children=i['name'],
                    href='mailto:' + i['email']
                ),
                " - " + i['desc']
            ],
            style={'list-style-type': 'disc'}
        ))
    return html.Ul(html_coords)


def build_subfooter():
    subfooter = html.Div([
        html.Br(),
        html.Hr(),
        html.Div(
            [
                # Contact part
                html.P([html.U('Contacts'), ' :'], style={'font-size': '1rem'}),
                build_contact_section([
                    {'name': 'Charles David WAJENBERG ', 'email': 'cwajnberg@myges.fr', 'desc': 'Project Owner'},
                    {'name': 'Jugurtha BOUHADOUN', 'email': 'jbouhadoun@gmail.com ', 'desc': 'Data Scientist'},
                    {'name': 'Djamel RAAB', 'email': 'djamel.r.75@gmail.com', 'desc': 'Data Engineer'},
                    {'name': 'Anis BAAR', 'email': 'mohamed.anis.barr@gmail.com', 'desc': 'Data Engineer'},
                ])
            ],
            className='mini_container'
        ),
        html.Div(
            [
                # Version part
                html.P([html.U('Version'), ' :'], style={'font-size': '1rem'}),
                html.Ul([
                    html.Li(
                        [html.A(
                            children='En cours de développement')
                         ],
                        style={'list-style-type': 'disc'}
                    ),
                    html.Li(
                        [html.A(children='Dernière modification le 30/04/2021')
                         ],
                        style={'list-style-type': 'disc'}
                    )])
            ],
            className='mini_container'
        )
    ])

    return subfooter


def build_sidebar():
    sidebar = html.Div([
        build_Footer(),
        html.H2(gv.APP_TITLE),
        html.Hr(),
        dbc.Nav(
            get_page_menu(),
            vertical=True,
            pills=True
        ),
        build_subfooter()
    ],
        style=gv.SIDEBAR_STYLE,
    )

    return sidebar
