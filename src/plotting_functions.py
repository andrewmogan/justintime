from dash import html
import plotly.graph_objects as go
from PIL import Image
from matplotlib import cm
from matplotlib.colors import Normalize
import numpy as np
import plotly.express as px
import rich
from all_data import trigger_record_data
from plotly.subplots import make_subplots
from all_data import trigger_record_data
from dash_bootstrap_templates import load_figure_template

def add_dunedaq_annotation(figure):
	figure.add_annotation(dict(font=dict(color="black",size=12),
		#x=x_loc,
		# x=1,
		# y=-0.20,
		x=1,
		y=1.20,
		showarrow=False,
		align="right",
		text='Powered by DUNE-DAQ',
		textangle=0,
		xref="paper",
		yref="paper"
		))

def selection_line(raw_data_file, trigger_record):
	return(html.Div([html.Hr(),
		html.B("selected raw data file:"),
		html.Br(),html.Div(raw_data_file),
		html.Br(),html.B("selected trigger record:"),
		html.Br(),html.Div(trigger_record),html.Hr()]))

def make_static_img(df,zmin: int = None, zmax: int = None, title: str = ""):

	xmin, xmax = min(df.columns), max(df.columns)
	#ymin, ymax = min(df.index), max(df.index)
	ymin, ymax = max(df.index), min(df.index)
	col_range = list(range(ymax, ymin))
	
	df = df.reindex(index=col_range, fill_value=0)

	img_width = df.columns.size
	img_height = df.index.size

	a = df.to_numpy()
	amin = zmin if zmin is not None else np.min(a)
	amax = zmax if zmax is not None else np.max(a)

	# Some normalization from matplotlib
	col_norm = Normalize(vmin=amin, vmax=amax)
	scalarMap  = cm.ScalarMappable(norm=col_norm, cmap='plasma' )
	seg_colors = scalarMap.to_rgba(a) 
	img = Image.fromarray(np.uint8(seg_colors*255))

	# Create figure
	fig = go.Figure()

	# Add invisible scatter trace.
	# This trace is added to help the autoresize logic work.
	# We also add a color to the scatter points so we can have a colorbar next to our image
	fig.add_trace(
		go.Scatter(
			x=[xmin, xmax],
			y=[ymin, ymax],
			mode="markers",
			marker={"color":[amin, amax],
					"colorscale":'Plasma',
					"showscale":True,
					"colorbar":{
						# "title":"Counts",
						"titleside": "right"
					},
					"opacity": 0
				}
		)
	)

	# Add image


	fig.update_layout(
		images=[go.layout.Image(
			x=xmin,
			sizex=xmax-xmin,
			y=ymax,
			sizey=ymax-ymin,
			xref="x",
			yref="y",
			opacity=1.0,
			layer="below",
			sizing="stretch",
			source=img)]
	)

	# Configure other layout
	fig.update_layout(
		title=title,
		xaxis=dict(showgrid=False, zeroline=False, range=[xmin, xmax]),
		yaxis=dict(showgrid=False, zeroline=False, range=[ymin, ymax]),
		yaxis_title="Offline Channel",
		xaxis_title="Time ticks")

	# fig.show(config={'doubleClick': 'reset'})
	return fig


def make_tp_plot(df, xmin, xmax, cmin, cmax, fig_w, fig_h, info):
	if not df.empty:
		# fig=go.Figure()
		fig= make_subplots(
			rows=1, cols=2, 
			#subplot_titles=(["Trigger Primitives"]), 
			column_widths=[0.2,0.9],
			horizontal_spacing=0.05,
			shared_yaxes=True,
			y_title="Offline Channel",
			x_title="Time Ticks",
		
		)
		fig.add_trace(
			go.Scattergl(
				y=df['offline_ch'],
				x=df['peak_time'],
				mode='markers',name="TP Trace",
				marker=dict(
					size=10,
					color=df['peak_adc'], #set color equal to a variable
					colorscale='Plasma', # one of plotly colorscales
					cmin = cmin,
					cmax = cmax,
					showscale=True
					),
				),
				row=1, col=2
			)
		fig.add_trace(
		go.Histogram(y=df["offline_ch"],name='channel', nbinsy=(xmax-xmin)), 
		row=1, col=1,
		)
		
		fig.update_yaxes(range=[xmin,xmax])
		fig.update_layout(legend=dict(yanchor="top", y=0.01, xanchor="left", x=1))

	else:
		fig = go.Figure()
		fig.add_trace(
			go.Scatter(
				y=[xmin, xmax],
				mode="markers",
			)
		)
	fig.update_layout(
		#width=fig_w,
		height=fig_h,
		yaxis = dict(autorange="reversed"),
		title_text=f"Run {info['run_number']}: {info['trigger_number']}",
		#legend=dict(x=0,y=1),
		width=950

		)

	return fig

def tp_for_adc(df, cmin, cmax):
	if not df.empty:
		# fig=go.Figure()
		fig=go.Scattergl(
				y=df['offline_ch'],
				x=df['peak_time'],
				mode='markers',name="TP Trace",
				marker=dict(
					size=4.5,
					color=df['peak_adc'], #set color equal to a variable
					colorscale="Turbo", # one of plotly colorscales
					cmin = cmin,
					cmax = cmax,
					showscale=True,
					
					
					),
				)
				
	

	else:
		fig =go.Scatter()
	
	return fig


def tp_density(df,xmin, xmax,cmin,cmax,fig_w, fig_h, info):
	if not df.empty:
		# fig=go.Figure()
		fig=px.density_heatmap(df,y=df['offline_ch'],
			x=df['peak_time'],nbinsy=200,nbinsx=200,
				z=df['peak_adc'],histfunc="count",
				color_continuous_scale="Plasma")

		fig.update_layout(
    xaxis_title="Time Ticks",
    yaxis_title="Offline Channel")
						
	else:
		fig = go.Figure()
		fig.add_trace(
			go.Scatter(
			
			)
		)
	fig.update_layout(
		#width=fig_w,
		height=fig_h,
		yaxis = dict(autorange="reversed"),
		title_text=f"Run {info['run_number']}: {info['trigger_number']}",
		legend=dict(x=0,y=1),
		width=950

		)
	fig.update_layout(font_family="Lato", title_font_family="Lato")
	return fig


def waveform_tps(data,channel_num):
	fig= px.line(data.df_cnr,y=channel_num)
	if channel_num in set(data.tp_df_tsoff['offline_ch']):
							
		rich.print("Data after CNR:")
		rich.print(data.df_cnr)
		new=(data.tp_df_tsoff.loc[data.tp_df_tsoff['offline_ch'] == channel_num])
		rich.print("Dataframe used for TPs (with similar offline channels)")
		rich.print(new)	
		rich.print("TPs time over threshold (in order of appearance):")					
		for i in range(len(new)):
																			
			time_start = new.iloc[i]['start_time']
			time_over_threshold = new.iloc[i]["time_over_threshold"]
			time_end = (new.iloc[i]["start_time"]+new.iloc[i]["time_over_threshold"])
			time_peak = new.iloc[i]["peak_time"]
			channel =new.iloc[i]["offline_ch"]
			adc_peak = new.iloc[i]["peak_adc"]
			rich.print(time_over_threshold)
								
			fig.add_vrect((time_start-time_peak)+time_start, (time_end-time_peak)+time_start, line_color="red")	
	return fig



def nothing_to_plot():

	return "Nothing to plot"