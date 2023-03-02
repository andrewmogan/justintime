from .. import ctrl_class
from dash import html, dcc
from cruncher.datamanager import DataManager
import rich
from dash.dependencies import Input, Output, State


def return_obj(dash_app, engine):
	ctrl_id = "04_partition_select_ctrl"
	data=engine.get_session_run_files_map()
	ctrl_div = html.Div([
	
		dcc.Dropdown(options=list(data.keys()),placeholder="Select Partition",
			id=ctrl_id),

        dcc.Store("partition_storage_id")
	],style={"marginBottom":"1.5em"})

	ctrl = ctrl_class.ctrl("name", ctrl_id, ctrl_div, engine)
	

	init_callbacks(dash_app,engine, data)
	return(ctrl)


	
def init_callbacks(dash_app, engine,data):
	@dash_app.callback(
		Output('partition_storage_id', 'data'),
		Input('04_partition_select_ctrl', 'value')
		)


	def store_subset(selection):
		if not selection:
			return {}
		subset = data[selection]
		return(subset)

