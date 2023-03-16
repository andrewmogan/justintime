from dash import html, dcc
from dash.dependencies import Input, Output, State
import rich
import plotly.express as px
from .. import ctrl_class
from ... cruncher.datamanager import DataManager

def return_obj(dash_app, engine):

	ctrl_id = "09_colorscale_ctrl"

	ctrl_div = html.Div([
		html.Div([
		html.Label("Select a Colorscale for ADC Map: ",style={"fontSize":"12px"}),
		html.Div([
		
		dcc.Dropdown(options=["plasma","RdBu_r"],value='plasma',
			id="colorscale_ctrl", clearable=False
		),
       
	],style={"marginBottom":"1.0em"})])],id=ctrl_id)

	ctrl = ctrl_class.ctrl("colorscale_select", ctrl_id, ctrl_div, engine)


	return(ctrl)