from .. import ctrl_class
from dash import html, dcc
from dash.dependencies import Input, Output, State

def return_obj(dash_app, engine):
	ctrl_id = "10_offset_ctrl"

	ctrl_div = html.Div([dcc.Checklist(options=["offset_removal"], value = ["offset_removal"],id=ctrl_id)],style={"marginBottom":"0.2em"})

	ctrl = ctrl_class.ctrl("offset", ctrl_id, ctrl_div, engine)

	return(ctrl)
