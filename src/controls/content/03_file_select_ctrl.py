from .. import ctrl_class
from dash import html, dcc


def return_obj(dash_app, engine):
	ctrl_id = "03_file_select_ctrl"

	ctrl_div = html.Div([
		dcc.Dropdown(
			id=ctrl_id,
			 options=[{'label': f, 'value':f} for f in sorted(engine.list_files(), reverse=True)]
		)
	])

	ctrl = ctrl_class.ctrl("file_select", ctrl_id, ctrl_div, engine)

	return(ctrl)