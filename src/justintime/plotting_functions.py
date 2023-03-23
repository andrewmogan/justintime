from dash import html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from PIL import Image
from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np
import rich

from . all_data import trigger_record_data

def add_dunedaq_annotation(figure):
	figure.add_annotation(dict(font=dict(color="black",size=12),
		#x=x_loc,
		# x=1,
		# y=-0.20,
		x=1,
		y=1.14,
		showarrow=False,
		align="right",
		text='Powered by DUNE-DAQ',
		textangle=0,
		xref="paper",
		yref="paper"
		))

def selection_line(partition,run,raw_data_file, trigger_record):
	return(html.Div([
		html.Div([
        html.B("Partition: ",style={"display":"inline-block",'marginRight':"0.4rem"}),
        html.Div(partition,style={"display":"inline-block"})]),
	
		html.Div([
        html.B("Run: ",style={"display":"inline-block",'marginRight':"0.4rem"}),
        html.Div(run,style={"display":"inline-block"})]),
	
		html.Div([
        html.B("Raw Data File: ",style={"display":"inline-block",'marginRight':"0.4rem"}),
        html.Div(raw_data_file,style={"display":"inline-block"})]),

		html.Div([
		html.B("Trigger Record: ",style={"display":"inline-block",'marginRight':"0.4rem"}),
		html.Div(trigger_record,style={"display":"inline-block"})])
		,html.Hr()
	]))

def make_static_img(df, zmin: int = None, zmax: int = None, title: str = "",colorscale:str="", height:int=600):
	
	if not df.empty:
		
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
		scalarMap  = cm.ScalarMappable(norm=col_norm, cmap=colorscale )
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
						"colorscale":colorscale,
						"showscale":True,
						"colorbar":{
							# "title":"Counts",
							"titleside": "right"
						},
						"opacity": 0
					},
                showlegend=False
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
			xaxis_title="Time ticks",
			height=height)
	else:
		
		fig=go.Figure()
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
                mode='markers',name="Trigger Primitives",
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
       # width=950
        )

    return fig

def tp_for_adc(df, cmin, cmax, orientation):

    if orientation == 'hd':
        x_label = 'peak_time'
        y_label = 'offline_ch'
    elif orientation == 'vd':
        x_label = 'offline_ch'
        y_label = 'peak_time'
    else:
        raise ValueError(f"Unexpeced orientation value found {orientation}. Expected values [hd, vd]")

    if not df.empty:
        rich.print(2.*max(df['sum_adc'])/(10**2))
        rich.print(max(df['sum_adc']))
        fig=go.Scattergl(
                x=df[x_label],
                y=df[y_label],
                # error_x=dict(
                # 	type='data',
                # 	symmetric=False,
                # 	array=df['peak_time']-df["start_time"],
                # 	arrayminus=df["time_over_threshold"]-(df['peak_time']-df["start_time"])
                # ),
                mode='markers',name="Trigger Primitives",
                
                marker=dict(size=df["sum_adc"],
                    sizemode='area',
                    sizeref=2.*max(df['sum_adc'])/(12**2),sizemin=3,
                    color=df['peak_adc'], #set color equal to a variable
                    colorscale="delta", # one of plotly colorscales
                    cmin = 0,
                    cmax = cmax,
                    showscale=True,colorbar=dict( x=1.12 )
                    ),
                text=[
                    f"start : {row['start_time']}<br>peak : {row['peak_time']}<br>end : {row['start_time']+row['time_over_threshold']}<br>tot : {row['time_over_threshold']}<br>offline ch: {row['offline_ch']}<br>sum adc : {row['sum_adc']}<br>peak adc : {row['peak_adc']}"
                        for index, row in df.iterrows()
                    ],
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
        fig = px.scatter()      
    
    fig.update_layout(
        #width=fig_w,
        height=fig_h,
        yaxis = dict(autorange="reversed"),
        title_text=f"Run {info['run_number']}: {info['trigger_number']}",
        legend=dict(x=0,y=1),
      #  width=950

        )
    fig.update_layout(font_family="Lato", title_font_family="Lato")
    return fig

def waveform_tps(fig,df,channel_num):
    if not df.empty:
        # fig=go.Figure()
        
        if channel_num in set(df['offline_ch']):            
            
            new=(df[df['offline_ch'] == channel_num])
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
                                    
                fig.add_vrect(time_start, time_end, line_width=0, fillcolor="red", opacity=0.2)
                fig.add_vline(x=time_peak, line_width=1, line_dash="dash", line_color="red")    
    else:
        fig = go.Scatter()
        
    return fig

def tp_hist_for_mean_std(df, xmin, xmax, info):
    if not df.empty:
        fig=go.Histogram(x=df["offline_ch"],name='TP Multiplicity per channel', nbinsx=(xmax-xmin))

    else:
        fig = go.Scatter()
 

    return fig

def nothing_to_plot():

    return "Nothing to plot"
