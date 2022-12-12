from .. import plot_class
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import numpy as np
import rich
from dash_bootstrap_templates import ThemeSwitchAIO
import pandas as pd
from all_data import trigger_record_data
from plotting_functions import add_dunedaq_annotation, selection_line, make_static_img,nothing_to_plot

def return_obj(dash_app, engine, storage,theme):
	plot_id = "10_trigger_record_display_plot"
	plot_div = html.Div(id = plot_id)
	plot = plot_class.plot("fft_plot", plot_id, plot_div, engine, storage,theme)
	plot.add_ctrl("04_trigger_record_select_ctrl")
	plot.add_ctrl("90_plot_button_ctrl")
	plot.add_ctrl("06_adc_map_selection_ctrl")
	plot.add_ctrl("07_tr_colour_range_slider_ctrl")
	plot.add_ctrl("08_static_image_ctrl")
	plot.add_ctrl("10_offset_ctrl")

	init_callbacks(dash_app, storage, plot_id, engine,theme)
	return(plot)

def init_callbacks(dash_app, storage, plot_id, engine,theme):

	@dash_app.callback(
		Output(plot_id, "children"),
		Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
		Input("90_plot_button_ctrl", "n_clicks"),
		State('04_trigger_record_select_ctrl', "value"),
		State('03_file_select_ctrl', "value"),
		State("06_adc_map_selection_ctrl", "value"),
		State("07_tr_colour_range_slider_comp", "value"),
		State("08_static_image_ctrl", "value"),
		State("10_offset_ctrl", "value"),
		State(plot_id, "children"),
	)
	def plot_trd_graph(theme,n_clicks, trigger_record, raw_data_file, adcmap_selection, tr_color_range, static_image, offset,original_state):
		theme = "cosmo" if  theme else "superhero"
		if trigger_record and raw_data_file:
			if plot_id in storage.shown_plots:
				data = storage.get_trigger_record_data(trigger_record, raw_data_file)
				if len(data.df)!=0:
					fig_w, fig_h = 1500, 1000
					children = []
					fzmin, fzmax = tr_color_range

					if 'Z' in adcmap_selection:
					 #trigger_record_data(engine,trigger_record,raw_data_file).t0_min
						if "offset_removal" in offset:
							title = "Z-plane offset removal,  Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)
							if "make_static_image" in static_image:
								fig = make_static_img((data.df_Z - data.df_Z_mean).T, theme,zmin = fzmin, zmax = fzmax,title=title)
							else:
								fig = px.imshow((data.df_Z - data.df_Z_mean).T, zmin=fzmin, zmax=fzmax, title=title,aspect="auto")
								fig.update_layout(
									width=fig_w,
									height=fig_h,template=theme
								)
								
							
						else:
							title = f"Z-plane: Run {data.info['run_number']}: {data.info['trigger_number']}, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)
						
							if "make_static_image" in static_image:
								fig = make_static_img(data.df_Z.T, theme,zmin = fzmin, zmax = fzmax, title = title)
								
							else:
								fig = px.imshow(data.df_Z.T, title=title, aspect='auto')
								fig.update_layout(
									width=fig_w,
									height=fig_h,template=theme
								)
						add_dunedaq_annotation(fig)
						children += [
							html.B("ADC Counts: Z-plane"),
							html.Hr(),
							dcc.Graph(figure=fig),
						]

					if 'V' in adcmap_selection:
						if "offset_removal" in offset:
							title = "V-plane offset removal,  Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)
							if "make_static_image" in static_image:
								fig = make_static_img((data.df_V - data.df_V_mean).T, theme,zmin = fzmin, zmax = fzmax, title = title)
							else:
								fig = px.imshow((data.df_V - data.df_V_mean).T, zmin=fzmin, title=title, aspect='auto')
								fig.update_layout(
									width=fig_w,
									height=fig_h,template=theme
								)
						else:
							title = f"V-plane: Run {data.info['run_number']}: {data.info['trigger_number']}, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)
							if "make_static_image" in static_image:
								fig = make_static_img(data.df_V.T,theme, zmin = fzmin, zmax = fzmax, title = title)
							else:
								fig = px.imshow(data.df_V.T, title=title, aspect='auto')
								fig.update_layout(
									width=fig_w,
									height=fig_h,template=theme
								)
				
						add_dunedaq_annotation(fig)
						children += [
							html.B("ADC Counts: V-plane"),
							html.Hr(),
							dcc.Graph(figure=fig),
						]

					if 'U' in adcmap_selection:
						if "offset_removal" in offset:
							title ="U-plane offset removal,  Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)
							if "make_static_image" in static_image:
								fig = make_static_img((data.df_U - data.df_U_mean).T, theme,zmin = fzmin, zmax = fzmax, title = title)
							else:
								fig = px.imshow((data.df_U - data.df_U_mean).T, zmin=fzmin, title=title, aspect="auto")
								
								fig.update_layout(
									width=fig_w,
									height=fig_h,template=theme
								)
						else:
							title = f"U-plane: Run {data.info['run_number']}: {data.info['trigger_number']}, Initial TS:"+str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)
							if "make_static_image" in static_image:
								fig = make_static_img(data.df_U.T, theme, zmin = fzmin, zmax = fzmax, title = title)
							else:
								fig = px.imshow(data.df_U.T, title=title, aspect='auto')
								fig.update_layout(
									width=fig_w,
									height=fig_h,template=theme
								)
						add_dunedaq_annotation(fig)
						children += [
							html.B("ADC Counts: U-plane"),
							html.Hr(),
							dcc.Graph(figure=fig),
						]

					if adcmap_selection:
						return(html.Div([
							selection_line(raw_data_file, trigger_record),
							html.Hr(),
							html.Div(children)]))
					else:
						return(html.Div("No adc map selected"))
				else:
					return(html.Div(html.H6(nothing_to_plot())))
			return(original_state)
		return(html.Div())
