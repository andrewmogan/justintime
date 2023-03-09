from dash import html, dcc
from dash.dependencies import Input, Output, State

from .. import ctrl_class

def return_obj(dash_app, engine):
	ctrl_id = "09_tr_colour_range_slider_ctrl"
	comp_id = "09_tr_colour_range_slider_comp"

	ctrl_div = html.Div([
		dcc.RangeSlider(
			id= comp_id,
			min=-1024,
			max=1024,
			step=64,
			value=[-192, 192],
			marks={ v:f"{v}" for v in range(-1024, 1025, 256) },
			
		)
	], id = ctrl_id)

	ctrl = ctrl_class.ctrl("coulr_range_slider", ctrl_id, ctrl_div, engine)

	return(ctrl)

