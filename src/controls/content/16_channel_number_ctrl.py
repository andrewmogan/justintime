from .. import ctrl_class
from dash import html, dcc
from dash.dependencies import Input, Output, State
from all_data import trigger_record_data
import rich


def return_obj(dash_app, engine):
	ctrl_id = "16_channel_number_ctrl"

	ctrl_div = html.Div([
		dcc.Dropdown(placeholder="Channel Number",
			id=ctrl_id
		)
	],
			style={"marginBottom":"1em"},)

	ctrl = ctrl_class.ctrl("channel_num", ctrl_id, ctrl_div, engine)
	ctrl.add_ctrl("13_plane_radio_ctrl")
	ctrl.add_ctrl("06_file_select_ctrl")
	ctrl.add_ctrl("07_trigger_record_select_ctrl")

	init_callbacks(dash_app,engine )
	return(ctrl)

def init_callbacks(dash_app,engine):
	@dash_app.callback(
		Output('16_channel_number_ctrl', 'options'),
		Input('13_plane_radio_ctrl', 'value'),Input("07_trigger_record_select_ctrl", 'value'),Input('06_file_select_ctrl', 'value')
		)
	def update_select(plane,trigger_record,raw_data_file):
		if not plane:
			return [""]
		try: 
			if "Z" in plane:
				channel_num= [{'label':str(n), 'value':(n)} for n in (trigger_record_data(engine,trigger_record,raw_data_file).df_Z.columns)]
			if "V" in plane:
				channel_num= [{'label':str(n), 'value':(n)} for n in (trigger_record_data(engine,trigger_record,raw_data_file).df_V.columns)]
			if "U" in plane:
				channel_num=[{'label':str(n), 'value':(n)} for n in (trigger_record_data(engine,trigger_record,raw_data_file).df_U.columns)]
			return(channel_num)
		except RuntimeError:return([""])
