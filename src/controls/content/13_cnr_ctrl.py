from .. import ctrl_class
from dash import html, dcc
from dash.dependencies import Input, Output, State

def return_obj(dash_app, engine):
	ctrl_id = "13_cnr_ctrl"

	ctrl_div = html.Div([dcc.Checklist(options=["cnr_removal"], value = ["cnr_removal"],id=ctrl_id)])

	ctrl = ctrl_class.ctrl("cnr", ctrl_id, ctrl_div, engine)

	return(ctrl)
