from .. import ctrl_class
from dash import html, dcc
from cruncher.datamanager import DataManager
import rich
from dash.dependencies import Input, Output, State

def return_obj(dash_app, engine):
	ctrl_id = "05_run_select_ctrl"

	ctrl_div = html.Div([
		dcc.Dropdown(placeholder="Run Number",
			id=ctrl_id
		),
        dcc.Store("run_storage_id")
	],style={"marginBottom":"1.5em"})

	ctrl = ctrl_class.ctrl("run_select", ctrl_id, ctrl_div, engine)
	ctrl.add_ctrl("04_partition_select_ctrl")

	init_callbacks(dash_app, engine)
	return(ctrl)

def init_callbacks(dash_app, engine):
	@dash_app.callback(
		Output('05_run_select_ctrl', 'options'),
		Input('partition_storage_id', 'data')
		)
	def update_select(stored_value):
		if not stored_value:
			return []
		options = [{'label':str(n), 'value':str(n)} for n in stored_value]
		return(options)
        
	@dash_app.callback(
		Output('run_storage_id', 'data'),
		Input('05_run_select_ctrl', 'value'),
        State('partition_storage_id', 'data')
		)
	def store_subset(selection, parent_stored_value):
		if not selection:
			return {}
		subset = parent_stored_value[selection]
		return(subset)