import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction

import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib


def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Just-in-Time"),
            html.H3("(Proto)DUNE Prompt-Feedback"),
            html.Div(
                id="intro",
                children="Select the data file and the trigger record in it.",
            ),
        ],
    )



def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    clinic_list = ['aaa', 'bbb', 'ccc']
    admit_list = ['1', '2', '3']
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Raw Data File"),
            dcc.Dropdown(
                id="raw-data-file-select",
                multi=True,
            ),
            html.Br(),
            html.P("Select Trigger Record"),
            dcc.Dropdown(
                id="trigger-record-select",
                multi=True,
            ),
            html.Br(),
            # html.P("Select Check-In Time"),
            # dcc.DatePickerRange(
            #     id="date-picker-select",
            #     start_date=dt(2014, 1, 1),
            #     end_date=dt(2014, 1, 15),
            #     min_date_allowed=dt(2014, 1, 1),
            #     max_date_allowed=dt(2014, 12, 31),
            #     initial_visible_month=dt(2014, 1, 1),
            # ),
            # html.Br(),
            # html.Br(),
            # html.P("Select Admit Source"),
            # dcc.Dropdown(
            #     id="admit-select",
            #     options=[{"label": i, "value": i} for i in admit_list],
            #     value=admit_list[:],
            #     multi=True,
            # ),
            # html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )

def generate():
    return html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="four columns",
                children=[description_card(), generate_control_card()]
                + [
                    html.Div(
                        ["initial child"], id="output-clientside", style={"display": "none"}
                    )
                ],
            ),
            # Right column
            html.Div(
                id="right-column",
                className="eight columns",
                children=[
                    # Patient Volume Heatmap
                    html.Div(
                        id="patient_volume_card",
                        children=[
                            html.B("Patient Volume"),
                            html.Hr(),
                            dcc.Graph(id="patient_volume_hm"),
                        ],
                    ),
                ],
            ),
        ],
    )