from .. import plot_class
from dash import html, dcc
from cruncher import datamanager
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import numpy as np
import rich
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import pandas as pd
from all_data import trigger_record_data
from plotting_functions import add_dunedaq_annotation, selection_line, make_static_img, make_tp_plot,tp_density,nothing_to_plot


def return_obj(dash_app, engine, storage,theme):
	plot_id = "01_tp_display_plot"
	plot_div = html.Div(id = plot_id)
	plot = plot_class.plot("fft_plot", plot_id, plot_div, engine, storage,theme)
	
	plot.add_ctrl("04_trigger_record_select_ctrl")
	plot.add_ctrl("90_plot_button_ctrl")
	plot.add_ctrl("07_tr_colour_range_slider_ctrl")
	plot.add_ctrl("12_density_plot_ctrl")
	plot.add_ctrl('02_description_ctrl')
	
	init_callbacks(dash_app, storage, plot_id, engine,theme)
	return(plot)

def init_callbacks(dash_app, storage, plot_id, engine,theme):
	
	@dash_app.callback(
		Output(plot_id, "children"),
		#Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
		Input("90_plot_button_ctrl", "n_clicks"),
		State('04_trigger_record_select_ctrl', "value"),
		State('03_file_select_ctrl', "value"),
		State("07_tr_colour_range_slider_comp", "value"),
		State('12_density_plot_ctrl', "value"),
		State('02_description_ctrl',"style"),
		State(plot_id, "children"),
	)
	def plot_tp_graph(n_clicks, trigger_record, raw_data_file, tr_color_range, density,description,original_state):
		load_figure_template(str(theme))
		if trigger_record and raw_data_file:
			if plot_id in storage.shown_plots:
				try: data = storage.get_trigger_record_data(trigger_record, raw_data_file)
				except RuntimeError: return(html.Div("Please choose both a run data file and trigger record"))
				
				
				if len(data.df)!=0 and len(data.df.index!=0):

					data.init_tp()
					fzmin, fzmax = tr_color_range
					fig_w, fig_h = 2600, 500
					children = []
					rich.print("TPs for Z plane:")
					rich.print(data.tp_df_Z)
					rich.print("TPs for V plane:")
					rich.print(data.tp_df_V)
					rich.print("TPs for U plane:")
					rich.print(data.tp_df_U)
					if "density_plot" in density:
						rich.print("2D Density plot chosen")
						fig = tp_density(data.tp_df_Z,data.xmin_Z, data.xmax_Z,fzmin,fzmax,fig_w, fig_h, data.info)
						children += [
							html.B("TPs: Z-plane, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
							#html.Hr(),
							dcc.Graph(figure=fig)]
						fig = tp_density(data.tp_df_V,data.xmin_V, data.xmax_V,fzmin,fzmax,fig_w, fig_h, data.info)
						children += [
							html.B("TPs: V-plane, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
							#html.Hr(),
							dcc.Graph(figure=fig)]
						
						fig = tp_density(data.tp_df_U,data.xmin_U, data.xmax_U,fzmin,fzmax,fig_w, fig_h, data.info)
						children += [
							html.B("TPs: U-plane,Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
							#html.Hr(),
							dcc.Graph(figure=fig)]

						fig = tp_density(data.tp_df_O,data.xmin_O, data.xmax_O,fzmin,fzmax,fig_w, fig_h, data.info)
						children += [
							html.B("TPs: Others, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
							#html.Hr(),
							dcc.Graph(figure=fig)]
					else:
						rich.print("Scatter Plot Chosen")
						fig = make_tp_plot(data.tp_df_Z,data.xmin_Z,data.xmax_Z, fzmin, fzmax, fig_w, fig_h, data.info)
						children += [
							html.B("TPs: Z-plane, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
							#html.Hr(),
							dcc.Graph(figure=fig),]
						fig = make_tp_plot(data.tp_df_V, data.xmin_V,data.xmax_V, fzmin, fzmax, fig_w, fig_h, data.info)
						children += [
							html.B("TPs: V-plane, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
							#html.Hr(),
							dcc.Graph(figure=fig)]
						
						fig = make_tp_plot(data.tp_df_U, data.xmin_U,data.xmax_U, fzmin, fzmax, fig_w, fig_h, data.info)
						children += [
							html.B("TPs: U-plane,Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
							#html.Hr(),
							dcc.Graph(figure=fig)]

						fig = make_tp_plot(data.tp_df_O,data.xmin_O,data.xmax_O, fzmin, fzmax, fig_w, fig_h, data.info)
						children += [
							html.B("TPs: Others, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)),
							#html.Hr(),
							dcc.Graph(figure=fig)]
					add_dunedaq_annotation(fig)
					return(html.Div([
						selection_line(raw_data_file, trigger_record),
						html.Div(children)]))
				else:
					return(html.Div(html.H6(nothing_to_plot())))
			return(original_state)
		return(html.Div())
