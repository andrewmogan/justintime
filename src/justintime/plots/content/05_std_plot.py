from dash import html, dcc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import rich
import numpy as np

from .. import plot_class
from ... plotting_functions import add_dunedaq_annotation, selection_line,nothing_to_plot


def return_obj(dash_app, engine, storage,theme):
	plot_id = "05_std_plot"
	plot_div = html.Div(id = plot_id)
	
	plot = plot_class.plot("std_plot", plot_id, plot_div, engine, storage,theme)
	
	plot.add_ctrl("partition_select_ctrl")
	plot.add_ctrl("run_select_ctrl")

	plot.add_ctrl("07_trigger_record_select_ctrl")
	plot.add_ctrl("90_plot_button_ctrl")

	init_callbacks(dash_app, storage, plot_id,theme)
	return(plot)

def init_callbacks(dash_app, storage, plot_id,theme):
	
	@dash_app.callback(
		Output(plot_id, "children"),
	##	Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
		Input("90_plot_button_ctrl", "n_clicks"),
		State("partition_select_ctrl","value"),
		State("run_select_ctrl","value"),
		State('trigger_record_select_ctrl', "value"),
		State('file_select_ctrl', "value"),
		State(plot_id, "children")
	)
	def plot_std_graph(n_clicks, partition,run,trigger_record, raw_data_file, original_state):

		load_figure_template(theme)
		if trigger_record and raw_data_file:
			if plot_id in storage.shown_plots:
				try: data = storage.get_trigger_record_data(trigger_record, raw_data_file)
				except RuntimeError: return(html.Div(""))
				
				if len(data.df)!=0 and len(data.df.index!=0):
					rich.print("STD Z-Plane")
					rich.print(data.df_Z_std)
					rich.print("STD V-Plane")
					rich.print(data.df_V_std)
					rich.print("STD U-Plane")
					rich.print(data.df_U_std)
					fig_std = make_subplots(rows=1, cols=3,
						subplot_titles=("STD U-Plane", "STD V-Plane", "STD Z-Plane"))
					fig_std.add_trace(
						go.Scattergl(x=data.df_U_std.index.astype(int), y=data.df_U_std, mode='markers', name=f"Run {data.info['run_number']}: {data.info['trigger_number']}"),
						row=1, col=1
					)
					fig_std.add_trace(
						go.Scattergl(x=data.df_V_std.index.astype(int), y=data.df_V_std, mode='markers', name=f"Run {data.info['run_number']}: {data.info['trigger_number']}"),
						row=1, col=2
					)
					fig_std.add_trace(
						go.Scattergl(x=data.df_Z_std.index.astype(int), y=data.df_Z_std, mode='markers', name=f"Run {data.info['run_number']}: {data.info['trigger_number']}"),
						row=1, col=3
					)

					fig_std.update_layout(
						# autosize=False,
						# width=1200,
						# height=600,
						margin=dict(
							l=50,
							r=50,
							b=100,
							t=100,
							pad=4
						)
						# showlegend=False
					)
					add_dunedaq_annotation(fig_std)
					fig_std.update_layout(font_family="Lato", title_font_family="Lato")
					return(html.Div([html.B("STD by plane"),dcc.Graph(figure=fig_std)]))
				else:
					return(html.Div(html.H6(nothing_to_plot())))
			return(original_state)
		return(html.Div())
