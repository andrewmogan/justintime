from .. import ctrl_class
from dash import html, dcc
from cruncher.datamanager import DataManager
import rich
from dash.dependencies import Input, Output, State

def return_obj(dash_app, engine):
	ctrl_id = "06_file_select_ctrl"

	ctrl_div = html.Div([
		dcc.Dropdown(placeholder="Data File",
			id=ctrl_id
		),
        dcc.Store("file_storage_id")
	],style={"marginBottom":"1.5em"})

	ctrl = ctrl_class.ctrl("file_select", ctrl_id, ctrl_div, engine)
	ctrl.add_ctrl("05_run_select_id")

	init_callbacks(dash_app, engine)
	return(ctrl)

def init_callbacks(dash_app, engine):
	@dash_app.callback(
		Output('06_file_select_ctrl', 'options'),
		Input('run_storage_id', 'data')
		)
	def update_select(stored_value):
		if not stored_value:
			return []
		options = [{'label':str(n), 'value':str(n)} for n in stored_value]
		return(options)
        
	@dash_app.callback(
		Output('file_storage_id', 'data'),
		Input('06_file_select_ctrl', 'value'),
        State('run_storage_id', 'data')
		)
	def store_subset(selection, parent_stored_value):
		if not selection:
			return {}
		rich.print("here")
		rich.print(selection)
		rich.print(parent_stored_value)
		#subset = parent_stored_value[selection]
		return(selection)