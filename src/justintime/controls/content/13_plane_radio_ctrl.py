from dash import html, dcc
from dash.dependencies import Input, Output, State

from .. import ctrl_class

def return_obj(dash_app, engine):
	ctrl_id = "13_plane_radio_ctrl"

	ctrl_div = html.Div([
		dcc.RadioItems(
			id=ctrl_id,
			options=[
				{'label': 'Z', 'value': 'Z'},
				{'label': 'V', 'value': 'V'},
				{'label': 'U', 'value': 'U'},
			],
			
			labelStyle={'display': 'inline-block',"marginRight":"0.2em","fontSize": "1.5rem"},
			style={'display': 'inline-block',"marginRight":"0.2em","fontSize": "1.5rem"},
		)
	])

	ctrl = ctrl_class.ctrl("plane_radio", ctrl_id, ctrl_div, engine)

	return(ctrl)