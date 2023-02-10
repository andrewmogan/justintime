from .. import ctrl_class
from dash import html, dcc
from dash.dependencies import Input, Output, State
from all_data import trigger_record_data
import rich


def return_obj(dash_app, engine):
	ctrl_id = "14_channel_number_ctrl"

	ctrl_div = html.Div([
		dcc.Dropdown(
			id=ctrl_id
		)
	],
			style={"marginBottom":"1em"},)

	ctrl = ctrl_class.ctrl("channel_num", ctrl_id, ctrl_div, engine)
	ctrl.add_ctrl("11_plane_radio_ctrl")
	ctrl.add_ctrl("03_file_select_ctrl")
	ctrl.add_ctrl("04_trigger_record_select_ctrl")

	init_callbacks(dash_app,engine )
	return(ctrl)

def init_callbacks(dash_app,engine):
	@dash_app.callback(
		Output('14_channel_number_ctrl', 'options'),
		Input('11_plane_radio_ctrl', 'value'),Input("04_trigger_record_select_ctrl", 'value'),Input('03_file_select_ctrl', 'value')
		)
	def update_select(plane,trigger_record,raw_data_file):
		if not plane:
			return [""]
		
		if "Z" in plane:
				channel_num= [{'label':str(n), 'value':(n)} for n in (trigger_record_data(engine,trigger_record,raw_data_file).df_Z.columns)]
		#rich.print(trigger_record_data(engine,trigger_record,raw_data_file).df_U)
		rich.print(trigger_record_data(engine,trigger_record,raw_data_file).df_U.columns)
		if "V" in plane:
				channel_num= [{'label':str(n), 'value':(n)} for n in (trigger_record_data(engine,trigger_record,raw_data_file).df_V.columns)]
		if "U" in plane:
				channel_num=[{'label':str(n), 'value':(n)} for n in (trigger_record_data(engine,trigger_record,raw_data_file).df_U.columns)]
		return(channel_num)
