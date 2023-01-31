from .. import ctrl_class
from dash import html, dcc
from dash.dependencies import Input, Output, State

def return_obj(dash_app, engine):
	ctrl_id = "14_channel_number_ctrl"

	ctrl_div = html.Div([
		dcc.Dropdown(
			id=ctrl_id
		)
	])

	ctrl = ctrl_class.ctrl("channel_num", ctrl_id, ctrl_div, engine)
	ctrl.add_ctrl("11_plane_radio_ctrl")

	init_callbacks(dash_app, )
	return(ctrl)

def init_callbacks(dash_app):
	@dash_app.callback(
		Output('14_channel_number_ctrl', 'options'),
		Input('11_plane_radio_ctrl', 'value')
		)
	def update_select(plane):
		if not plane:
			return [""]
		
		if "Z" in plane:
				channel_num= [{'label':str(n), 'value':(n)} for n in range(0,800)]
		if "V" in plane:
				channel_num= [{'label':str(n), 'value':(n)} for n in range(800,1600)]
		if "U" in plane:
				channel_num=[{'label':str(n), 'value':(n)} for n in range(1600,2560)]
		return(channel_num)
