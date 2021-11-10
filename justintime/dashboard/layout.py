from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ClientsideFunction

import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib
from os.path import splitext


def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Just-in-Time"),
            html.H4("(Proto)DUNE"),
            html.H4("Prompt-Feedback"),
            html.Div(
                id="intro",
                children="Select data file and trigger record",
            ),
        ],
    )



def generate_control_card(brain):
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Raw Data File A"),
            dcc.Dropdown(
                id="raw-data-file-select-A",
                # multi=True,
                options=[{'label': f, 'value':f} for f in sorted(brain.list_files(), reverse=True)]
            ),
            html.Br(),
            html.P("Select Trigger Record A"),
            dcc.Dropdown(
                id="trigger-record-select-A",
                # multi=True,
            ),
            html.Br(),
            html.P("Select Raw Data File B"),
            dcc.Dropdown(
                id="raw-data-file-select-B",
                # multi=True,
                options=[{'label': f, 'value':f} for f in sorted(brain.list_files(), reverse=True)]
            ),
            html.Br(),
            html.P("Select Trigger Record B"),
            dcc.Dropdown(
                id="trigger-record-select-B",
                # multi=True,
            ),
            html.Br(),
            html.Button('Refresh Files', id='refresh_files', n_clicks=0),
            html.Button('Plot', id='plot_button', n_clicks=0),
            html.Br(),
            html.Br(),
            # html.P("Cached datasets"),
            
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

def generate(brain):
    return html.Div(
        id="app-container",
        children=[
            dcc.Location(id='url', refresh=False),
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=[description_card(), generate_control_card(brain)]
                + [
                    html.Div(
                        ["initial child"], id="output-clientside", style={"display": "none"}
                    )
                ],
            ),
            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    # Patient Volume Heatmap
                    html.Div(
                        id="mean_std_by_plane_card",
                        children=[
                            html.B("Hello"),
                            # html.Hr(),
                            # dcc.Graph(id="mean_std_plan_subplots"),
                        ],
                    ),
                ],
            ),
        ],
    )