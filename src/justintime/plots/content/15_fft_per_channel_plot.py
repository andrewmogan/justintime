from .. import plot_class
from dash import html, dcc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import rich
import pandas as pd

from ... plotting_functions import add_dunedaq_annotation, selection_line,waveform_tps,nothing_to_plot


def return_obj(dash_app, engine, storage,theme):
	plot_id = "15_fft_per_channel_plot"
	plot_div = html.Div(id = plot_id)
	plot = plot_class.plot("FFT_Channel_plot", plot_id, plot_div, engine, storage,theme)
	plot.add_ctrl("07_refresh_ctrl")
	plot.add_ctrl("partition_select_ctrl")
	plot.add_ctrl("run_select_ctrl")

	plot.add_ctrl("06_trigger_record_select_ctrl")
	plot.add_ctrl("09_tr_colour_range_slider_ctrl")
	plot.add_ctrl("16_channel_number_ctrl")
	plot.add_ctrl("90_plot_button_ctrl")

	init_callbacks(dash_app, storage, plot_id,theme)

	return(plot)

def init_callbacks(dash_app, storage, plot_id,theme):
	@dash_app.callback(
		Output(plot_id, "children"),
		##Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
		Input("90_plot_button_ctrl", "n_clicks"),
		State('07_refresh_ctrl', "value"),
		State('trigger_record_select_ctrl', "value"),
		State("partition_select_ctrl","value"),
		State("run_select_ctrl","value"),
		
		State('16_channel_number_ctrl',"value"),
		State("09_tr_colour_range_slider_comp", "value"),
		State('file_select_ctrl', "value"),
		
		State(plot_id, "children"),
	)
	def plot_fft_graph(n_clicks, refresh,trigger_record,partition,run,channel_num,tr_color_range,raw_data_file, original_state):
	
		load_figure_template(theme)
	

		if trigger_record and raw_data_file:
			if plot_id in storage.shown_plots:
				try: data = storage.get_trigger_record_data(trigger_record, raw_data_file)
				except RuntimeError: return(html.Div("Please choose both a run data file and trigger record"))

				rich.print("Initial Time Stamp:",data.t0_min)
				rich.print(" ")
				rich.print("Initial Dataframe:")
				rich.print(data.df_tsoff)
				
				if len(data.df)!=0 and len(data.df.index!=0):
					data.init_fft()
					if channel_num:
						if int(channel_num) in data.channels:

							fzmin, fzmax = tr_color_range
							rich.print("FFT of values:")
							rich.print(data.df_fft)
							rich.print("Channel number selected: ",channel_num)
							fig=px.line(data.df_fft,y=channel_num)
							rich.print("FFT for the selected channel values:")
							print(data.df_fft[channel_num])
							fig.update_layout(
								xaxis_title="Frequency",
								yaxis_title="FFT",
								#height=fig_h,
								title_text=f"Run {data.info['run_number']}: {data.info['trigger_number']}",
								legend=dict(x=0,y=1),
								width=950,

								)
							
							add_dunedaq_annotation(fig)
							fig.update_layout(font_family="Lato", title_font_family="Lato")
							return(html.Div([
									selection_line(partition,run,raw_data_file, trigger_record),
									html.B(f"FFT for channel {channel_num}"),
									#html.Hr(),
									dcc.Graph(figure=fig),
									]))
					else:
						return(html.Div(html.H6("No Channel Selected")))
				else:
					return(html.Div(html.H6(nothing_to_plot())))
					
			return(original_state)
		return(html.Div())
