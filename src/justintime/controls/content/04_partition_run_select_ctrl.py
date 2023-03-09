from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import rich

from .. import ctrl_class
from ... cruncher.datamanager import DataManager


def return_obj(dash_app, engine):
	ctrl_id = "04_partition_run_select_ctrl"
	data=engine.get_session_run_files_map()
	ctrl_div = html.Div(
		html.Div([
		html.Label("Select Partition and Run Number: ",style={"fontSize":"12px"}),
		dbc.Row([
		
		dbc.Col(html.Div([
	
		dcc.Dropdown(placeholder="Partition",
			id="partition_select_ctrl"), #options=list(data.keys())

        dcc.Store("partition_storage_id")
		],style={"marginBottom":"1.0em"})),

		dbc.Col(html.Div([
		
		dcc.Dropdown(placeholder="Run Number",
			id="run_select_ctrl"
		),
        dcc.Store("run_storage_id")],style={"marginBottom":"1.0em"}))
	])]),id=ctrl_id)
	
	
	ctrl = ctrl_class.ctrl("name", ctrl_id, ctrl_div, engine)
	ctrl.add_ctrl("03_refresh_ctrl")
	

	init_callbacks(dash_app,engine,data)
	return(ctrl)


	
def init_callbacks(dash_app, engine,data):
	@dash_app.callback(
		Output('partition_storage_id', 'data'),
		Input('partition_select_ctrl', 'value')
		)


	def store_subset(selection):
		if not selection:
			return {}
		subset = data[selection]
		return(subset)
	
	@dash_app.callback(
		Output('run_select_ctrl', 'options'),
		Input('partition_storage_id', 'data')
		)
	
	def update_select(stored_value):
		if not stored_value:
			return []
		options = [{'label':str(n), 'value':str(n)} for n in stored_value]
		return(options)
        
	@dash_app.callback(
		Output('run_storage_id', 'data'),
		Input('run_select_ctrl', 'value'),
        State('partition_storage_id', 'data')
		)
	
	def store_subset(selection, parent_stored_value):
		if not selection:
			return {}
		subset = parent_stored_value[selection]
		return(subset)

