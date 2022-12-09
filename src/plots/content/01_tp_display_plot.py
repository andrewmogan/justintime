from .. import plot_class
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import numpy as np
import rich
from dash_bootstrap_templates import load_figure_template
import pandas as pd
from all_data import trigger_record_data
from plotting_functions import add_dunedaq_annotation, selection_line, make_static_img, make_tp_plot,nothing_to_plot


def return_obj(dash_app, engine, storage):
	plot_id = "01_tp_display_plot"
	plot_div = html.Div(id = plot_id)
	load_figure_template("COSMO")
	plot = plot_class.plot("fft_plot", plot_id, plot_div, engine, storage)
	plot.add_ctrl("04_trigger_record_select_ctrl")
	plot.add_ctrl("90_plot_button_ctrl")
	plot.add_ctrl("07_tr_colour_range_slider_ctrl")

	init_callbacks(dash_app, storage, plot_id, engine)
	return(plot)

def init_callbacks(dash_app, storage, plot_id, engine):

	@dash_app.callback(
		Output(plot_id, "children"),
		Input("90_plot_button_ctrl", "n_clicks"),
		State('04_trigger_record_select_ctrl', "value"),
		State('03_file_select_ctrl', "value"),
		State("07_tr_colour_range_slider_comp", "value"),
		State(plot_id, "children"),
	)
	def plot_tp_graph(n_clicks, trigger_record, raw_data_file, tr_color_range, original_state):
		if trigger_record and raw_data_file:
			if plot_id in storage.shown_plots:
				data = storage.get_trigger_record_data(trigger_record, raw_data_file)
				rich.print(data.df)
				if len(data.df)!=0:
					data.init_tp()
					fzmin, fzmax = tr_color_range
					fig_w, fig_h = 1500, 1000
					children = []
					fig = make_tp_plot(data.tp_df_Z, data.xmin_Z, data.xmax_Z, fzmin, fzmax, fig_w, fig_h, data.info)
					children += [
						html.B("TPs: Z-plane, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
						html.Hr(),
						dcc.Graph(figure=fig)]

					fig = make_tp_plot(data.tp_df_V, data.xmin_V, data.xmax_V, fzmin, fzmax, fig_w, fig_h, data.info)
					children += [
						html.B("TPs: V-plane, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
						html.Hr(),
						dcc.Graph(figure=fig)]
					
					fig = make_tp_plot(data.tp_df_U, data.xmin_U, data.xmax_U, fzmin, fzmax, fig_w, fig_h, data.info)
					children += [
						html.B("TPs: U-plane,Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
						html.Hr(),
						dcc.Graph(figure=fig)]


					fig = make_tp_plot(data.tp_df_O, data.xmin_O, data.xmax_O, fzmin, fzmax, fig_w, fig_h, data.info)
					children += [
						html.B("TPs: Others, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
						html.Hr(),
						dcc.Graph(figure=fig)]
					
					return(html.Div([
						selection_line(raw_data_file, trigger_record),
						html.Hr(),
						html.Div(children)]))
				else:
					return(html.Div(html.H6(nothing_to_plot())))
			return(original_state)
		return(html.Div())
