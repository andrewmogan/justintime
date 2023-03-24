from dash import html, dcc
from dash.dependencies import Input, Output, State

from .. import ctrl_class

def return_obj(dash_app, engine):
    ctrl_id = "18_cnr_ctrl"

    ctrl_div = html.Div([dcc.Checklist([{"label":"cnr_removal","value":"cnr_removal"}],value=[],id=ctrl_id)],style={"marginBottom":"0.2em","fontSize": "1.5rem"})
    ctrl = ctrl_class.ctrl("cnr", ctrl_id, ctrl_div, engine)

    return(ctrl)
