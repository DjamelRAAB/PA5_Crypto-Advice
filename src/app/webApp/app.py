# coding: utf-8

"""

app
***************

This script initial dash app. In a multi page application, we need to share "app" variable
in several scripts, that's why we initiate it in a separete script.

"""

import dash

import global_variables as gv

app = dash.Dash(
    external_stylesheets=[
        './webapp/assets/s1.css',
        './webapp/assets/styles.css',
        gv.APP_THEME],
    routes_pathname_prefix= '/' + gv.NAME_APPLICATION + '/')
server = app.server
app.config.suppress_callback_exceptions = True
