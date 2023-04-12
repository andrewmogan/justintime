from dash import html, dcc
from dash.dependencies import Input, Output, State

from .. import ctrl_class

def return_obj(dash_app, engine, storage):
    ctrl_id = "21_tp_multiplicity_ctrl"

    ctrl_div = html.Div([dcc.Checklist(options=[{"label":"TP Multiplicity per Plane","value":"tp_multiplicity"}], value = ["tp_multiplicity"],id=ctrl_id)],style={"marginTop":"1em","fontSize": "1.5rem","marginBottom":"1.0em","fontSize": "1.5rem"})

    ctrl = ctrl_class.ctrl("tp_multiplicity", ctrl_id, ctrl_div, engine)

    return(ctrl)
