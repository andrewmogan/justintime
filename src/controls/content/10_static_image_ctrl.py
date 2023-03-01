from .. import ctrl_class
from dash import html, dcc
from dash.dependencies import Input, Output, State

def return_obj(dash_app, engine):
	ctrl_id = "10_static_image_ctrl"

	ctrl_div = html.Div([dcc.Checklist(options=["make_static_image"], value = ["make_static_image"],id=ctrl_id)],style={"marginBottom":"0.2em","marginTop":"1em"})

	ctrl = ctrl_class.ctrl("static_image", ctrl_id, ctrl_div, engine)

	return(ctrl)
