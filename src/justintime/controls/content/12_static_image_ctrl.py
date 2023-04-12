from dash import html, dcc
from dash.dependencies import Input, Output, State

from .. import ctrl_class

def return_obj(dash_app, engine, storage):
    ctrl_id = "12_static_image_ctrl"

    ctrl_div = html.Div([dcc.Checklist(options=[{"label":"Make Static Image","value":"make_static_image"}], value = ["make_static_image"],id=ctrl_id)],style={"marginTop":"1em","fontSize": "1.5rem"})

    ctrl = ctrl_class.ctrl("static_image", ctrl_id, ctrl_div, engine)

    return(ctrl)
