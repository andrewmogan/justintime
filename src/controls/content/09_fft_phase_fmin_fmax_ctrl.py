from .. import ctrl_class
from dash import html, dcc
from dash.dependencies import Input, Output, State

def return_obj(dash_app, engine):
	ctrl_id = "09_fft_phase_fmin_fmax_ctrl"
	comp_id_fmin = "09_fft_phase_fmin_comp"
	comp_id_fmax = "09_fft_phase_fmax_comp"

	ctrl_div = html.Div([
		html.Div("fmin"),
		dcc.Input(id=comp_id_fmin, type="number",placeholder="fmin"),
		html.Div("fmax"),
		dcc.Input(id=comp_id_fmax, type="number",placeholder="fmax"),
	], id=ctrl_id)

	ctrl = ctrl_class.ctrl("fmin_fmax", ctrl_id, ctrl_div, engine)

	return(ctrl)
