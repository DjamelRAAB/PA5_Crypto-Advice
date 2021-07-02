# coding: utf-8

"""

index
***************

Index.py is the main script of the web application. Its role is to detected which page is called
regarding url, build the whole page and serve it.

Locally, it's possible to launch the application with this script with the command :
        $ python index.py

The application will be available at http://localhost:8050

Please note that a proper mode is to launch it with launcher.py

"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import page_retriever as pr
import global_variables as gv
from datetime import datetime

content = html.Div(id="page-content", style=gv.CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), pr.build_sidebar(), content])


@app.callback(
    [Output(f"{page_id}", "active") for page_id in pr.APP_PAGES],
    [Input("url", "pathname")],
)
def show_active_page(pathname: str):
    """show_active_page selects which is the active page regarding apps URL and set show it.
    All other pages are set hidden.

    Args:
        pathname (str): url called

    Returns:
        list: the list is of number of pages length. Value is true for active page, false otherwise
    """
    return [pathname == f"{p}" for p in pr.PAGES_URLS]


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname: str):
    """render_page_content calls the right function to generate page content regarding given URL

    Args:
        pathname (str): URL called

    Returns:
        dash content : page content
    """
    for page in pr.APP_PAGES:
        if pathname == pr.APP_PAGES[page]['URL']:
            return pr.APP_PAGES[page]['Content']

    return pr.build_page_not_found()


# Add route to monitor availability of the app
@app.server.route('/')
def ping():
    # current date and time
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    log = {}
    log ["timestamp"] = int(timestamp)
    log ["status"] = "OK"
    return str(log)


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=5000, debug=True)
