from .. import plot_class
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import numpy as np
from dash_bootstrap_templates import ThemeSwitchAIO
import pandas as pd
import rich
from plotting_functions import add_dunedaq_annotation, selection_line,nothing_to_plot


def return_obj(dash_app, engine, storage):
	plot_id = "07_fft_phase_plot"
	plot_div = html.Div(id = plot_id)
	plot = plot_class.plot("fft_plot", plot_id, plot_div, engine, storage)
	plot.add_ctrl("04_trigger_record_select_ctrl")
	plot.add_ctrl("09_fft_phase_fmin_fmax_ctrl")
	plot.add_ctrl("90_plot_button_ctrl")

	init_callbacks(dash_app, storage, plot_id, engine)
	return(plot)

def init_callbacks(dash_app, storage, plot_id, engine):

	@dash_app.callback(
		Output(plot_id, "children"),
		##Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
		Input("90_plot_button_ctrl", "n_clicks"),
		State('04_trigger_record_select_ctrl', "value"),
		State('03_file_select_ctrl', "value"),
		State('09_fft_phase_fmin_comp', "value"),
		State('09_fft_phase_fmax_comp', "value"),
		State(plot_id, "children"),
	)
	def plot_fft_phase_graph(n_clicks, trigger_record, raw_data_file, fmin, fmax, original_state):
		##theme = "darkly" if  theme else "superhero"
		load_figure_template("darkly")
		if trigger_record and raw_data_file:
			if plot_id in storage.shown_plots:
				try: data = storage.get_trigger_record_data(trigger_record, raw_data_file)
				except RuntimeError: return(html.Div("Please choose both a run data file and trigger record"))
				
				if len(data.df)!=0:
					rich.print(data.fft_phase)
					data.init_fft_phase(fmin, fmax)

					fig = px.scatter(data.fft_phase[f"{fmin}-{fmax}"], y='phase', color=data.fft_phase[f"{fmin}-{fmax}"]['femb'].astype(str), labels={'color':'FEMB ID'}, facet_col='plane', facet_col_wrap=2, facet_col_spacing=0.03, facet_row_spacing=0.07, title=f"Trigger record: Run {data.info['run_number']}, {data.info['trigger_number']} fmin = {fmin}, fmax = {fmax}")
					fig.update_xaxes(matches=None, showticklabels=True)
					fig.update_yaxes(matches=None, showticklabels=True)
					fig.update_layout(height=900)
					add_dunedaq_annotation(fig)
					return(html.Div([
						selection_line(raw_data_file, trigger_record),
						html.B("Noise phase by FEMB peak"),
						html.Hr(),
						dcc.Graph(figure=fig)]))
				else:
					return(html.Div(html.H6(nothing_to_plot())))

			return(original_state)

		return(html.Div())
