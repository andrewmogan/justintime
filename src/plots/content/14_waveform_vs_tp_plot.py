from .. import plot_class
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
from dash_bootstrap_templates import ThemeSwitchAIO
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import numpy as np
import rich
import pandas as pd
from plotting_functions import add_dunedaq_annotation, selection_line,waveform_tps,nothing_to_plot


def return_obj(dash_app, engine, storage):
	plot_id = "14_waveform_vs_tp_plot"
	plot_div = html.Div(id = plot_id)
	plot = plot_class.plot("waveform_tp_plot", plot_id, plot_div, engine, storage)
	plot.add_ctrl("04_trigger_record_select_ctrl")


	plot.add_ctrl("07_tr_colour_range_slider_ctrl")
	plot.add_ctrl("14_channel_number_ctrl")
	plot.add_ctrl("90_plot_button_ctrl")

	init_callbacks(dash_app, storage, plot_id)

	return(plot)

def init_callbacks(dash_app, storage, plot_id):
	@dash_app.callback(
		Output(plot_id, "children"),
		##Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
		Input("90_plot_button_ctrl", "n_clicks"),
		State('04_trigger_record_select_ctrl', "value"),
		State('14_channel_number_ctrl',"value"),
		State("07_tr_colour_range_slider_comp", "value"),
		State('03_file_select_ctrl', "value"),
		
		State(plot_id, "children"),
	)
	def plot_fft_graph(n_clicks, trigger_record,channel_num,tr_color_range,raw_data_file, original_state):
		#theme = "darkly" if  theme else "superhero"
		load_figure_template("darkly")
		fir_shift = 16

		if trigger_record and raw_data_file:
			if plot_id in storage.shown_plots:
                
				data = storage.get_trigger_record_data(trigger_record, raw_data_file)
				data.init_tp()
				data.init_cnr()
				print(data.tp_df_tsoff)
				if len(data.df)!=0:
					
					if int(channel_num) in data.channels:
						
						fzmin, fzmax = tr_color_range
						title_U=f"FFT U-plane: Run {data.info['run_number']}: {data.info['trigger_number']}" 
						print(set(data.tp_df_tsoff['offline_ch']))
						fig=waveform_tps(data,channel_num)

						fig.update_layout(
							xaxis_title="Time Ticks",
    						yaxis_title="ADC Waveform",
							#height=fig_h,
							title_text=f"Run {data.info['run_number']}: {data.info['trigger_number']}",
							legend=dict(x=0,y=1),
							width=950,

							)
						
						add_dunedaq_annotation(fig)
							
						return(html.Div([
								selection_line(raw_data_file, trigger_record),
								html.B(f"Waveform and TPs for channel {channel_num}"),
								html.Hr(),
								dcc.Graph(figure=fig),
								]))
					else:
						return(html.Div(html.H6(nothing_to_plot())))
					
				return(original_state)
			return(html.Div())
