from .. import ctrl_class
from dash import html, dcc
from dash.dependencies import Input, Output, State

def return_obj(dash_app, engine):
	ctrl_id = "08_adc_map_selection_ctrl"

	ctrl_div = html.Div([
		dcc.Checklist(
			id=ctrl_id,
			options=[
				{'label': 'Z', 'value': 'Z'},
				{'label': 'V', 'value': 'V'},
				{'label': 'U', 'value': 'U'},
			],
			value=[],
			labelStyle={'display': 'inline-block',"marginRight":"0.2em"},
			style={'display': 'inline-block',"marginRight":"0.2em"},
		)
	],style={"marginBottom":"1em","fontSize": "1.35rem"})

	ctrl = ctrl_class.ctrl("adc_map_selection", ctrl_id, ctrl_div, engine)

	return(ctrl)

