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
            html.P("Raw Data File A"),
            dcc.Dropdown(
                id="raw-data-file-select-A",
                # multi=True,
                options=[{'label': f, 'value':f} for f in sorted(brain.list_files(), reverse=True)]
            ),
            # html.Br(),
            html.P("Trigger Record A"),
            dcc.Dropdown(
                id="trigger-record-select-A",
                # multi=True,
            ),
            html.Br(),
            html.P("Raw Data File B"),
            dcc.Dropdown(
                id="raw-data-file-select-B",
                # multi=True,
                options=[{'label': f, 'value':f} for f in sorted(brain.list_files(), reverse=True)]
            ),
            # html.Br(),
            html.P("Trigger Record B"),
            dcc.Dropdown(
                id="trigger-record-select-B",
                # multi=True,
            ),
            html.Br(),
            html.P("Plots"),
            dcc.Checklist(
                id='plot_selection',
                options=[
                    {'label': 'Mean & STD', 'value': 'Mean_STD'},
                    {'label': 'Fourier Transform', 'value': 'FFT'},
                ],
                value=['Mean_STD', 'FFT']
            ),
            html.Br(),
            html.P("ADC Maps"),
            html.Div(
                'TR A planes :',
                style={'display': 'inline-block'}
            ),
            dcc.Checklist(
                id='adcmap-selection-a',
                options=[
                    {'label': 'Z', 'value': 'Z'},
                    {'label': 'V', 'value': 'V'},
                    {'label': 'U', 'value': 'U'},
               ],
                value=[],
                labelStyle={'display': 'inline-block'},
                style={'display': 'inline-block'},
            ),
            html.Br(),
            html.Div(
                'TR B planes : ',
                style={'display': 'inline-block'}
            ),
            dcc.Checklist(
                id='adcmap-selection-b',
                options=[
                    {'label': 'Z', 'value': 'Z'},
                    {'label': 'V', 'value': 'V'},
                    {'label': 'U', 'value': 'U'},
               ],
                value=[],
                labelStyle={'display': 'inline-block'},
                style={'display': 'inline-block'},
            ),
            html.Br(),
            html.Div(
                'TR (A-B) planes : ',
                style={'display': 'inline-block'}
            ),
            dcc.Checklist(
                id='adcmap-selection-ab-diff',
                options=[
                    {'label': 'Z', 'value': 'Z'},
                    {'label': 'V', 'value': 'V'},
                    {'label': 'U', 'value': 'U'},
               ],
                value=[],
                labelStyle={'display': 'inline-block'},
                style={'display': 'inline-block'},
            ),
            html.Br(),
            html.Div(
                'TR A (self-subtracted) planes : ',
                style={'display': 'inline-block'}
            ),
            dcc.Checklist(
                id='adcmap-selection-a-filt-x',
                options=[
                    {'label': 'Z', 'value': 'Z'},
                    {'label': 'V', 'value': 'V'},
                    {'label': 'U', 'value': 'U'},
               ],
                value=[],
                labelStyle={'display': 'inline-block'},
                style={'display': 'inline-block'},
            ),
            html.Br(),
            html.P("color bar range"),
            dcc.RangeSlider(
                id='ab-diff-range-slider',
                min=-2048,
                max=2048,
                step=64,
                value=[-320, 192],
                marks={ v:f"{v}" for v in range(-2048, 2049, 512) }
            ),
            html.Br(),
            html.Button('Refresh Files', id='refresh_files', n_clicks=0),
            html.Button('Plot', id='plot_button', n_clicks=0),
            html.Br(),
            html.Br(),

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
    
                            html.H1("DUNE Prompt Feedback", className="display-3"),
                            html.P(
                                "Minimal plotting service to asses raw data quality just-in-time.",
                                className="lead",
                            ),
        
                        ],
                    ),
                ],
            ),
        ],
    )