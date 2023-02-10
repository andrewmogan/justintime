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
from plotting_functions import add_dunedaq_annotation, selection_line, make_static_img,nothing_to_plot,make_tp_plot,tp_for_adc

def return_obj(dash_app, engine, storage,theme):
	plot_id = "13_adc_tp_plot"
	plot_div = html.Div(id = plot_id)
	plot = plot_class.plot("fft_plot", plot_id, plot_div, engine, storage,theme)
	plot.add_ctrl("04_trigger_record_select_ctrl")
	plot.add_ctrl("90_plot_button_ctrl")
	plot.add_ctrl("06_adc_map_selection_ctrl")
	plot.add_ctrl("07_tr_colour_range_slider_ctrl")
	plot.add_ctrl("08_static_image_ctrl")
	plot.add_ctrl("10_offset_ctrl")
	plot.add_ctrl("13_cnr_ctrl")

	init_callbacks(dash_app, storage, plot_id, engine,theme)
	return(plot)

def init_callbacks(dash_app, storage, plot_id, engine,theme):

	@dash_app.callback(
		Output(plot_id, "children"),
		##Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
		Input("90_plot_button_ctrl", "n_clicks"),
		State('04_trigger_record_select_ctrl', "value"),
		State('03_file_select_ctrl', "value"),
		State("06_adc_map_selection_ctrl", "value"),
		State("07_tr_colour_range_slider_comp", "value"),
		State("08_static_image_ctrl", "value"),
		State("10_offset_ctrl", "value"),
		State("13_cnr_ctrl", "value"),
		State(plot_id, "children"),
	)
	def plot_trd_graph(n_clicks, trigger_record, raw_data_file, adcmap_selection, tr_color_range, static_image, offset,cnr,original_state):
		
		load_figure_template(theme)
		if trigger_record and raw_data_file:
			if plot_id in storage.shown_plots:
				try: data = storage.get_trigger_record_data(trigger_record, raw_data_file)
				except RuntimeError: return(html.Div("Please choose both a run data file and trigger record"))
				
				if len(data.df)!=0:
					data.init_tp()
					data.init_cnr()
					fig_w, fig_h = 1500, 1000
					children = []
					fzmin, fzmax = tr_color_range

					if 'Z' in adcmap_selection:
						rich.print("Z Plane selected")
						if "cnr_removal" in cnr:
							rich.print("CNR selected")
							rich.print("Raw ADCs:")
							rich.print(data.df_cnr[data.planes.get(2, {})].T)
							rich.print("TPs:")
							rich.print(data.tp_df_Z)
							title = f"Z-plane (CNR): Run {data.info['run_number']}: {data.info['trigger_number']} "

							if "make_static_image" in static_image:
								fig = make_static_img(data.df_cnr[data.planes.get(2, {})].T, zmin = fzmin, zmax = fzmax, title = title)
								fig.add_trace(tp_for_adc(data.tp_df_Z, fzmin,fzmax))
							else:
								fig = px.imshow(data.df_cnr[data.planes.get(2, {})].T, zmin=fzmin, zmax=fzmax, title=title, aspect='auto')
								fig.add_trace(tp_for_adc(data.tp_df_Z, fzmin,fzmax))
								fig.update_layout(
										width=900,
										height=800,yaxis_title="Offline Channel",
										xaxis_title="Time ticks",showlegend=True
										)
						else:
							if "offset_removal" in offset:
								rich.print("Offset removal selected")
								rich.print("Raw ADCs:")
								rich.print((data.df_Z - data.df_Z_mean).T)
								rich.print("TPs:")
								rich.print(data.tp_df_Z)
								title = f"Z-plane offset removal, Run {data.info['run_number']}: {data.info['trigger_number']}"
								if "make_static_image" in static_image:
									fig = make_static_img((data.df_Z - data.df_Z_mean).T, zmin = fzmin, zmax = fzmax,title=title)
									fig.add_trace(tp_for_adc(data.tp_df_Z, fzmin,fzmax))
				
								else:
									
									fig = px.imshow((data.df_Z - data.df_Z_mean).T, zmin=fzmin, zmax=fzmax, title=title,aspect="auto")
									fig.add_trace(tp_for_adc(data.tp_df_Z, fzmin,fzmax))
									fig.update_layout(
										width=900,
										height=800,yaxis_title="Offline Channel",
										xaxis_title="Time ticks",showlegend=True
										)

							else:
								rich.print("Raw ADCs:")
								rich.print(data.df_Z)
								rich.print("TPs:")
								rich.print(data.tp_df_Z)
								title = f"Z-plane, Run {data.info['run_number']}: {data.info['trigger_number']}"
							
								if "make_static_image" in static_image:
									fig = make_static_img(data.df_Z.T,zmin = fzmin, zmax = fzmax, title = title)
									fig.add_trace(tp_for_adc(data.tp_df_Z, fzmin,fzmax))
									
								else:
									fig = px.imshow(data.df_Z.T, title=title, aspect='auto')
									fig.add_trace(tp_for_adc(data.tp_df_Z, fzmin,fzmax))
									fig.update_layout(
										width=900,
										height=800,yaxis_title="Offline Channel",
										xaxis_title="Time ticks",showlegend=True
									)
						add_dunedaq_annotation(fig)
						fig.update_layout(font_family="Lato", title_font_family="Lato")
						children += [
							html.B(f"ADC Counts: Z-plane, Initial TS: {str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)}"),
							html.Hr(),
							dcc.Graph(figure=fig),
						]
						fig.update_layout(legend=dict(yanchor="top", y=0.01, xanchor="left", x=1))
					
					if 'V' in adcmap_selection:
						rich.print("V Plane selected")
						if "cnr_removal" in cnr:
							rich.print("CNR selected")
							rich.print("Raw ADCs:")
							rich.print(data.df_cnr[data.planes.get(1, {})].T)
							rich.print("TPs:")
							rich.print(data.tp_df_V)
							title = f"V-plane (CNR), Run {data.info['run_number']}: {data.info['trigger_number']}"

							if "make_static_image" in static_image:
								fig = make_static_img(data.df_cnr[data.planes.get(1, {})].T, zmin = fzmin, zmax = fzmax, title = title)
								fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
							else:
								fig = px.imshow(data.df_cnr[data.planes.get(1, {})].T, zmin=fzmin, zmax=fzmax, title=title, aspect='auto')
								fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
								fig.update_layout(
										width=900,
										height=800,yaxis_title="Offline Channel",
										xaxis_title="Time ticks",showlegend=True
										)
						else:
							if "offset_removal" in offset:
								rich.print("Offset removal selected")
								rich.print("Raw ADCs:")
								rich.print((data.df_V - data.df_V_mean).T)
								rich.print("TPs:")
								rich.print(data.tp_df_V)
								title = f"V-plane offset removal,  Run {data.info['run_number']}: {data.info['trigger_number']}"
								if "make_static_image" in static_image:
									fig = make_static_img((data.df_V - data.df_V_mean).T, zmin = fzmin, zmax = fzmax,title=title)
									fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
				
								else:
									fig = px.imshow((data.df_V - data.df_V_mean).T, zmin=fzmin, zmax=fzmax, title=title,aspect="auto")
									fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
									fig.update_layout(
										width=900,
										height=800,yaxis_title="Offline Channel",
										xaxis_title="Time ticks",showlegend=True
										)

							else:
								rich.print("Raw ADCs:")
								rich.print(data.df_V)
								rich.print("TPs:")
								rich.print(data.tp_df_V)
								title = f"V-plane, Run {data.info['run_number']}: {data.info['trigger_number']}"
							
								if "make_static_image" in static_image:
									fig = make_static_img(data.df_V.T,zmin = fzmin, zmax = fzmax, title = title)
									fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
									
								else:
									fig = px.imshow(data.df_V.T, title=title, aspect='auto')
									fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
									fig.update_layout(
										width=900,
										height=800,yaxis_title="Offline Channel",
										xaxis_title="Time ticks",showlegend=True
									)
				
						add_dunedaq_annotation(fig)
						fig.update_layout(font_family="Lato", title_font_family="Lato")
						children += [
							html.B(f"ADC Counts: V-plane, Initial TS: {str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)}"),
							html.Hr(),
							dcc.Graph(figure=fig),
						]
						fig.update_layout(legend=dict(yanchor="top", y=0.01, xanchor="left", x=1))
					if 'U' in adcmap_selection:
						rich.print("U Plane selected")
						if "cnr_removal" in cnr:
							rich.print("CNR selected")
							rich.print("Raw ADCs:")
							rich.print(data.df_cnr[data.planes.get(0, {})].T)
							rich.print("TPs:")
							rich.print(data.tp_df_U)
							title = f"U-plane (CNR): Run {data.info['run_number']}: {data.info['trigger_number']}"

							if "make_static_image" in static_image:
								fig = make_static_img(data.df_cnr[data.planes.get(0, {})].T, zmin = fzmin, zmax = fzmax, title = title)
								fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
							else:
								fig = px.imshow(data.df_cnr[data.planes.get(0, {})].T, zmin=fzmin, zmax=fzmax, title=title, aspect='auto')
								fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
								fig.update_layout(
										width=900,
										height=800,yaxis_title="Offline Channel",
										xaxis_title="Time ticks",showlegend=True
										)
						else:
							if "offset_removal" in offset:
								rich.print("Offset removal selected")
								rich.print("Raw ADCs:")
								rich.print((data.df_U - data.df_U_mean).T)
								rich.print("TPs:")
								rich.print(data.tp_df_U)
								title = f"U-plane offset removal, Run {data.info['run_number']}: {data.info['trigger_number']}"
								if "make_static_image" in static_image:
									fig = make_static_img((data.df_U - data.df_U_mean).T, zmin = fzmin, zmax = fzmax,title=title)
									fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
				
								else:
									fig = px.imshow((data.df_U - data.df_U_mean).T, zmin=fzmin, zmax=fzmax, title=title,aspect="auto")
									fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
									fig.update_layout(
										width=900,
										height=800,yaxis_title="Offline Channel",
										xaxis_title="Time ticks",showlegend=True
										)

							else:
								rich.print("Raw ADCs:")
								rich.print(data.df_U)
								rich.print("TPs:")
								rich.print(data.tp_df_U)
								title = f"U-plane, Run {data.info['run_number']}: {data.info['trigger_number']}"
							
								if "make_static_image" in static_image:
									fig = make_static_img(data.df_U.T,zmin = fzmin, zmax = fzmax, title = title)
									fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
									
								else:
									fig = px.imshow(data.df_U.T, title=title, aspect='auto')
									fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
									fig.update_layout(
										width=900,
										height=800,yaxis_title="Offline Channel",
										xaxis_title="Time ticks",showlegend=True
									)
						add_dunedaq_annotation(fig)
						fig.update_layout(font_family="Lato", title_font_family="Lato")
						children += [
							html.B(f"ADC Counts: U-plane, Initial TS: {str(trigger_record_data(engine,trigger_record,raw_data_file).t0_min)}"),
							html.Hr(),
							dcc.Graph(figure=fig),
						]
						fig.update_layout(legend=dict(yanchor="top", y=0.01, xanchor="left", x=1))
					if adcmap_selection:
						return(html.Div([
							selection_line(raw_data_file, trigger_record),
							html.Hr(),
							html.Div(children)]))
					else:
						return(html.Div("No ADC map selected"))
					
				else:
					return(html.Div(html.H6(nothing_to_plot())))
			return(original_state)
		return(html.Div())
