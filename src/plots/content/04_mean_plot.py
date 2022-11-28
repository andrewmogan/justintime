from .. import plot_class
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import numpy as np
from plotting_functions import add_dunedaq_annotation, selection_line


def return_obj(dash_app, engine, storage):
	plot_id = "04_mean_plot"
	plot_div = html.Div(id = plot_id)

	plot = plot_class.plot("Mean_plot", plot_id, plot_div, engine, storage)
	plot.add_ctrl("04_trigger_record_select_ctrl")
	plot.add_ctrl("90_plot_button_ctrl")

	init_callbacks(dash_app, storage, plot_id)
	return(plot)

def init_callbacks(dash_app, storage, plot_id):
	@dash_app.callback(
		Output(plot_id, "children"),
		Input("90_plot_button_ctrl", "n_clicks"),
		State('04_trigger_record_select_ctrl', "value"),
		State('03_file_select_ctrl', "value"),
		State(plot_id, "children")
	)
	def plot_mean_graph(n_clicks, trigger_record, raw_data_file, original_state):
		if trigger_record and raw_data_file:
			if plot_id in storage.shown_plots:
				data = storage.get_trigger_record_data(trigger_record, raw_data_file)

				fig_mean = make_subplots(rows=1, cols=3,
					subplot_titles=("Mean U-Plane", "Mean V-Plane", "Mean Z-Plane"))
				fig_mean.add_trace(
					go.Scattergl(x=data.df_U_mean.index.astype(int), y=data.df_U_mean, mode='markers', name=f"Run {data.info['run_number']}: {data.info['trigger_number']}"),
					row=1, col=1
				)
				fig_mean.add_trace(
					go.Scattergl(x=data.df_V_mean.index.astype(int), y=data.df_V_mean, mode='markers', name=f"Run {data.info['run_number']}: {data.info['trigger_number']}"),
					row=1, col=2
				)
				fig_mean.add_trace(
					go.Scattergl(x=data.df_Z_mean.index.astype(int), y=data.df_Z_mean, mode='markers', name=f"Run {data.info['run_number']}: {data.info['trigger_number']}"),
					row=1, col=3
				)

				fig_mean.update_layout(
					# autosize=False,
					# width=1200,
					# height=600,
					margin=dict(
						l=50,
						r=50,
						b=100,
						t=100,
						pad=4
					),
					# showlegend=False
				)
				add_dunedaq_annotation(fig_mean)

				return(html.Div([selection_line(raw_data_file, trigger_record),html.B("Mean by plane"),html.Hr(),dcc.Graph(figure=fig_mean)]))
			return(original_state)
		return(html.Div())
