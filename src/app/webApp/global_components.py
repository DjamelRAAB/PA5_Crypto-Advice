# coding: utf-8

"""

global_components
*****************

This script defines functions that build some classic components such as input controls, plots...
This allow us to factorize code.

"""
import base64

import dash_html_components as html
import dash_core_components as dcc


def get_dropdown(drop_id: str, drop_options: list='', drop_default: str='',
                 place_hold: str='', multi_select: bool=False):
    """get_dropdown builds a dash dropdown control

    Args:
        drop_id (str): dropdown id
        drop_options (list, optional): A list of options {label: [string|number], value: [string|number]} 
                                      to feed the dropdown.
        drop_default (str, optional): Dropdown default value. Default to empty value.
        place_hold (str, optional): The grey, default text shown when no option is selected. 
        multi_select (bool, optional): If true, the user can select multiple values. Defaults to False.

    Returns:
        dropdown control: Returns a dropdown dash core component
    """
    drop = dcc.Dropdown(
        id=drop_id,
        options=drop_options,
        value=drop_default,
        multi=multi_select,
        placeholder=place_hold
    )

    return drop


def get_radio(radio_id: str, radio_options: list, radio_default: str=None, horizontal: bool=False):
    """get_radio builds a dash radio button set control

    Args:
        radio_id (str): radio button id
        radio_options (list): A list of options {label: [string|number], value: [string|number]}
                              to feed the radio buttons.
        radio_default (str, optional): Radio button default value. Default to empty value.
        horizontal (bool, optional): If true dispose options horizontally, side by side.
                                     If false, dispose options vertically. lDefaults to False.

    Returns:
        radio button control: Returns a radion button dash core component
    """
    if horizontal:
        display = 'inline-block'
    else:
        display = 'block'

    radio = dcc.RadioItems(
        id=radio_id,
        options=radio_options,
        value=radio_default,
        labelStyle={'display': display}
    )

    return radio


def get_checkbox(check_id: str, check_options: list, check_default: list=[], horizontal: bool=False):
    """get_checkbox builds a dash check box set control

    Args:
        check_id (str): check box id
        check_options (list): A list of options {label: [string|number], value: [string|number]} 
                              to feed the radio buttons.
        check_default (list, optional): Options checked by default. Defaults to [].
        horizontal (bool, optional): If true dispose options horizontally, side by side. 
                                     If false, dispose options vertically. lDefaults to False.

    Returns:
        check box control: Returns a check box dash core component
    """
    if horizontal:
        display = 'inline-block'
    else:
        display = 'block'

    check = dcc.Checklist(
        id=check_id,
        options=check_options,
        value=check_default,
        labelStyle={'display': display,
                    'padding-right': '10px'
                    }
    )

    return check


def get_image(img_path: str, height: int, width: int):
    """get_image [summary]

    Args:
        path (str): [description]
        height (int): [description]
        width (int): [description]
    """
    img_encoded = base64.b64encode(open(img_path, 'rb').read())

    image = html.A([ 
                html.Img(src='data:image/png;base64,{}'.format(img_encoded.decode()),
                     height=height, width=width)
                ],
                href='http://127.0.0.1:8050/crypto-advice/'
            )
    return image
