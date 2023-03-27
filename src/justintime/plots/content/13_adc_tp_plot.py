from dash import html, dcc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import rich
import pandas as pd
import logging
from .. import plot_class
from ... all_data import trigger_record_data
from ... plotting_functions import add_dunedaq_annotation, selection_line, make_static_img,nothing_to_plot,make_tp_plot,tp_for_adc

def return_obj(dash_app, engine, storage,theme):
    plot_id = "13_adc_tp_plot"
    plot_div = html.Div(id = plot_id)
    plot = plot_class.plot("fft_plot", plot_id, plot_div, engine, storage,theme)
    plot.add_ctrl("07_refresh_ctrl")
    plot.add_ctrl("partition_select_ctrl")
    plot.add_ctrl("run_select_ctrl")
    plot.add_ctrl("06_trigger_record_select_ctrl")
    plot.add_ctrl("90_plot_button_ctrl")
    plot.add_ctrl("08_adc_map_selection_ctrl")
    plot.add_ctrl("09_colorscale_ctrl")
    plot.add_ctrl("10_tr_colour_range_slider_ctrl")
    plot.add_ctrl("12_static_image_ctrl")
    plot.add_ctrl("19_tp_overlay_ctrl")
    plot.add_ctrl("17_offset_ctrl")
    plot.add_ctrl("20_orientation_height_ctrl")
    #plot.add_ctrl("18_cnr_ctrl")

    init_callbacks(dash_app, storage, plot_id, engine,theme)
    return(plot)

def plot_adc_map(data, plane_id, colorscale, tr_color_range, static_image, offset, overlay_tps, orientation, height):
    fzmin, fzmax = tr_color_range
    ts_title =  'DTS time ticks (16ns)'
    och_title = 'Offline Channel'
    if "offset_removal" in offset:
        
        df_adc = (getattr(data, f'df_{plane_id}') - getattr(data,f'df_{plane_id}_mean'))
        
        if orientation == 'horizontal':
            df_adc = df_adc.T
            xaxis_title = ts_title
            yaxis_title = och_title
           
        elif orientation == 'vertical':
            xaxis_title = och_title
            yaxis_title = ts_title
           
        else:
            raise ValueError(f"Unexpeced orientation value found {orientation}. Expected values [horizontal, vertical]")

        df_tps = getattr(data, f'tp_df_{plane_id}')

        logging.info("Offset removal selected")
        logging.info(f"Raw ADCs in {plane_id}-Plane after offset removal:")
        logging.info(df_adc)
            
        title = f"{plane_id}-plane offset removal, Run {data.info['run_number']}: {data.info['trigger_number']}"
        if "make_static_image" in static_image:
            fig = make_static_img(df_adc, zmin = fzmin, zmax = fzmax, title=title, colorscale=colorscale, height=height,orientation=orientation)
            if "tp_overlay" in overlay_tps:
                logging.info(f"TPs in {plane_id}-Plane:")
                logging.info(df_tps)
                fig.add_trace(tp_for_adc(df_tps, fzmin, fzmax, orientation))
                rich.print(fzmin,fzmax)    

        else:
            rich.print(fzmin,fzmax)                                     
            fig = px.imshow(df_adc, zmin=fzmin, zmax=fzmax, title=title, color_continuous_scale=colorscale, aspect="auto")
            if "tp_overlay" in overlay_tps:
                    logging.info(f"TPs in {plane_id}-Plane:")
                    logging.info(df_tps)
                    fig.add_trace(tp_for_adc(df_tps, fzmin,fzmax, orientation))
        fig.update_layout(
                    height=height,
                    yaxis_title=yaxis_title,
                    xaxis_title=xaxis_title,
                    showlegend=True
                    )

    else:
            logging.info("Raw ADCs in Z-Plane:")
            df_adc = getattr(data, f"df_{plane_id}")

            if orientation == 'horizontal':
                df_adc = df_adc.T
                xaxis_title = ts_title
                yaxis_title = och_title
               
            elif orientation == 'vertical':
                xaxis_title = och_title
                yaxis_title = ts_title
               
            else:
                raise ValueError(f"Unexpeced orientation value found {orientation}. Expected values [horizontal, vertical]")
            
            df_tps = getattr(data, f'tp_df_{plane_id}')
            
            title = f"{plane_id}-plane, Run {data.info['run_number']}: {data.info['trigger_number']}"
        
            if "make_static_image" in static_image:
                fig = make_static_img(df_adc,zmin = fzmin, zmax = fzmax, title = title, colorscale=colorscale, height=height,orientation=orientation)
                if "tp_overlay" in overlay_tps: 
                    logging.info(f"TPs in {plane_id}-Plane:")
                    logging.info(df_tps)
                    fig.add_trace(tp_for_adc(df_tps, fzmin, fzmax, orientation))
                
            else:
                fig = px.imshow(df_adc, zmin=fzmin, zmax=fzmax,title=title, color_continuous_scale=colorscale, aspect='auto')
                if "tp_overlay" in overlay_tps:
                    logging.info(f"TPs in {plane_id}-Plane:")
                    logging.info(df_tps)
                    fig.add_trace(tp_for_adc(df_tps, fzmin,fzmax, orientation))
            fig.update_layout(
                        height=height,
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        showlegend=True
                )
    add_dunedaq_annotation(fig)
    fig.update_layout(font_family="Lato", title_font_family="Lato")

    fig.update_layout(legend=dict(yanchor="top", y=0.01, xanchor="left", x=1))

    children = [
        html.B(f"ADC Counts: {plane_id}-plane, Initial TS: {str(data.ts_min)}"),
        #html.Hr(),
        dcc.Graph(figure=fig,style={"marginTop":"10px","marginBottom":"10px"}),
    ]

    return children

def init_callbacks(dash_app, storage, plot_id, engine, theme):

    @dash_app.callback(
        Output(plot_id, "children"),
        Input("90_plot_button_ctrl", "n_clicks"),
        State('07_refresh_ctrl', "value"),
        State('trigger_record_select_ctrl', "value"),
        State('file_select_ctrl', "value"),
        State("partition_select_ctrl","value"),
        State("run_select_ctrl","value"),
        State("adc_map_selection_ctrl", "value"),
        State("colorscale_ctrl", "value"),
        State("10_tr_colour_range_slider_comp", "value"),
        State("12_static_image_ctrl", "value"),
        State("17_offset_ctrl", "value"),
        #State("18_cnr_ctrl", "value"),
        State("19_tp_overlay_ctrl","value"),
        State("orientation_ctrl","value"),
        State("height_select_ctrl","value"),
        State(plot_id, "children"),
    )
    def plot_trd_graph(n_clicks, refresh,trigger_record, raw_data_file, partition, run, adcmap_selection, colorscale, tr_color_range, static_image, offset, overlay_tps,orientation,height,original_state):
        
        load_figure_template(theme)
        orientation = orientation
        if trigger_record and raw_data_file:
            if plot_id in storage.shown_plots:
                try: data = storage.get_trigger_record_data(trigger_record, raw_data_file)
                except RuntimeError: return(html.Div("Please choose both a run data file and trigger record"))

                logging.info(f"Initial Time Stamp: {data.ts_min}")
                logging.info(" ")
                logging.info("Initial Dataframe:")
                logging.info(data.df_tsoff)
                
                if len(data.df)!=0 and len(data.df.index!=0):
                    data.init_tp()
                    # data.init_cnr()
                    rich.print(static_image,offset,overlay_tps,orientation,height)
                    children = []
                    if 'Z' in adcmap_selection:
                        logging.info("Z Plane selected")
                        children += plot_adc_map(data, 'Z', colorscale, tr_color_range, static_image, offset, overlay_tps, orientation,height)
                    if 'U' in adcmap_selection:
                        logging.info("U Plane selected")
                        children += plot_adc_map(data, 'U', colorscale, tr_color_range, static_image, offset, overlay_tps, orientation,height)
                    if 'V' in adcmap_selection:
                        logging.info("V Plane selected")
                        children += plot_adc_map(data, 'V', colorscale, tr_color_range, static_image, offset, overlay_tps, orientation,height)

                    # if 'Z' in adcmap_selection:
                        
                        """ if "cnr_removal" in cnr:
                            rich.print("CNR selected")
                            rich.print("Raw ADCs in Z-plane after CNR:")
                            rich.print(data.df_cnr[data.planes.get(2, {})].T)
                            
                            title = f"Z-plane (CNR): Run {data.info['run_number']}: {data.info['trigger_number']} "

                            if "make_static_image" in static_image:
                                fig = make_static_img(data.df_cnr[data.planes.get(2, {})].T, zmin = fzmin, zmax = fzmax, title = title)
                                if "tp_overlay" in overlay_tps:
                                    rich.print("TPs in Z-Plane:")
                                    rich.print(data.tp_df_Z)
                                    fig.add_trace(tp_for_adc(data.tp_df_Z, fzmin,fzmax))
                            else:
                                fig = px.imshow(data.df_cnr[data.planes.get(2, {})].T, zmin=fzmin, zmax=fzmax, title=title,  color_continuous_scale='plasma',aspect='auto')
                                if "tp_overlay" in overlay_tps:
                                    rich.print("TPs in Z-Plane:")
                                    rich.print(data.tp_df_Z)
                                    fig.add_trace(tp_for_adc(data.tp_df_Z, fzmin,fzmax))
                                fig.update_layout(
                                        
                                        height=600,yaxis_title="Offline Channel",
                                        xaxis_title="Time ticks",showlegend=True
                                        ) 
                        else:"""
                        # logging.info("Z Plane selected")
                        # plane_id = 'Z'

                        # if "offset_removal" in offset:
                            
                        #   df_adc = (data.df_Z - data.df_Z_mean)
                        #   if orientation == 'hd':
                        #       df_adc = df_adc.T
                        #   df_tps = data.tp_df_Z

                        #   logging.info("Offset removal selected")
                        #   logging.info(f"Raw ADCs in {plane_id}-Plane after offset removal:")
                        #   logging.info(df_adc)
                                
                        #   title = f"{plane_id}-plane offset removal, Run {data.info['run_number']}: {data.info['trigger_number']}"
                        #   if "make_static_image" in static_image:
                        #       fig = make_static_img(df_adc, zmin = fzmin, zmax = fzmax,title=title,colorscale=colorscale)
                        #       if "tp_overlay" in overlay_tps:
                        #           logging.info(f"TPs in {plane_id}-Plane:")
                        #           logging.info(df_tps)
                        #           fig.add_trace(tp_for_adc(df_tps, fzmin,fzmax))
                
                        #   else:
                                                                        
                        #       fig = px.imshow(df_adc, zmin=fzmin, zmax=fzmax, title=title,color_continuous_scale=colorscale,aspect="auto")
                        #       if "tp_overlay" in overlay_tps:
                        #               logging.info("TPs in Z-Plane:")
                        #               logging.info(df_tps)
                        #               fig.add_trace(tp_for_adc(df_tps, fzmin,fzmax, orientation))
                        #               fig.update_layout(
                        #               height=600,yaxis_title="Offline Channel",
                        #               xaxis_title="Time ticks",showlegend=True
                        #               )

                        # else:
                        #       logging.info("Raw ADCs in Z-Plane:")
                        #       df_adc = data.df_Z
                        #       if orientation == 'hd':
                        #           df_adc = df_adc.T
                        #       logging.info(df_adc)
                        #       df_tps = data.tp_df_Z

                                
                        #       title = f"Z-plane, Run {data.info['run_number']}: {data.info['trigger_number']}"
                            
                        #       if "make_static_image" in static_image:
                        #           fig = make_static_img(df_adc,zmin = fzmin, zmax = fzmax, title = title,colorscale=colorscale)
                        #           if "tp_overlay" in overlay_tps: 
                        #               logging.info(f"TPs in {plane_id}-Plane:")
                        #               logging.info(df_tps)
                        #               fig.add_trace(tp_for_adc(df_tps, fzmin,fzmax))
                                    
                        #       else:
                        #           fig = px.imshow(df_adc,  zmin=fzmin, zmax=fzmax,title=title, color_continuous_scale=colorscale,aspect='auto')
                        #           if "tp_overlay" in overlay_tps:
                        #               logging.info(f"TPs in {plane_id}-Plane:")
                        #               logging.info(df_tps)
                        #               fig.add_trace(tp_for_adc(df_tps, fzmin,fzmax, orientation))
                        #           fig.update_layout(
                                        
                        #               height=600,yaxis_title="Offline Channel",
                        #               xaxis_title="Time ticks",showlegend=True
                        #           )
                        # add_dunedaq_annotation(fig)
                        # fig.update_layout(font_family="Lato", title_font_family="Lato")
                        # children += [
                        #   html.B(f"ADC Counts: {plane_id}-plane, Initial TS: {str(trigger_record_data(engine,trigger_record,raw_data_file).ts_min)}"),
                        #   #html.Hr(),
                        #   dcc.Graph(figure=fig,style={"marginTop":"10px","marginBottom":"10px"}),
                        # ]
                        # fig.update_layout(legend=dict(yanchor="top", y=0.01, xanchor="left", x=1))
                    
                    # if 'V' in adcmap_selection:
                    #   logging.info("V Plane selected")
                    #   """if "cnr_removal" in cnr:
                    #       rich.print("CNR selected")
                    #       rich.print("Raw ADCs in V-Plane after CNR:")
                    #       rich.print(data.df_cnr[data.planes.get(1, {})].T)
                            
                    #       title = f"V-plane (CNR), Run {data.info['run_number']}: {data.info['trigger_number']}"

                    #       if "make_static_image" in static_image:
                    #           fig = make_static_img(data.df_cnr[data.planes.get(1, {})].T, zmin = fzmin, zmax = fzmax, title = title)
                    #           if "tp_overlay" in overlay_tps:
                    #               rich.print("TPs in V-Plane:")
                    #               rich.print(data.tp_df_V)
                    #               fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
                    #       else:
                    #           fig = px.imshow(data.df_cnr[data.planes.get(1, {})].T, zmin=fzmin, zmax=fzmax, title=title, color_continuous_scale='plasma',aspect='auto')
                    #           if "tp_overlay" in overlay_tps:
                    #               rich.print("TPs in V-Plane:")
                    #               rich.print(data.tp_df_V)
                    #               fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
                    #           fig.update_layout(
                                        
                    #                   height=600,yaxis_title="Offline Channel",
                    #                   xaxis_title="Time ticks",showlegend=True
                    #                   )
                    #       else:"""
                    #   if "offset_removal" in offset:
                    #           logging.info("Offset removal selected")
                    #           logging.info("Raw ADCs in V-Plane after offset removal:")
                    #           logging.info((data.df_V - data.df_V_mean).T)
                    #           logging.info("TPs in V-Plane:")
                    #           logging.info(data.tp_df_V)
                    #           title = f"V-plane offset removal,  Run {data.info['run_number']}: {data.info['trigger_number']}"
                    #           if "make_static_image" in static_image:
                    #               fig = make_static_img((data.df_V - data.df_V_mean).T, zmin = fzmin, zmax = fzmax,title=title,colorscale=colorscale)
                    #               if "tp_overlay" in overlay_tps:
                    #                   fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
                
                    #           else:
                    #               fig = px.imshow((data.df_V - data.df_V_mean).T, zmin=fzmin, zmax=fzmax, title=title,color_continuous_scale=colorscale,aspect="auto")
                    #               if "tp_overlay" in overlay_tps:
                    #                   logging.info("TPs in V-Plane:")
                    #                   logging.info(data.tp_df_V)
                    #                   fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
                    #               fig.update_layout(
                                        
                    #                   height=600,yaxis_title="Offline Channel",
                    #                   xaxis_title="Time ticks",showlegend=True
                    #                   )

                    #   else:
                    #           logging.info("Raw ADCs in V-Plane:")
                    #           logging.info(data.df_V)
                                
                    #           title = f"V-plane, Run {data.info['run_number']}: {data.info['trigger_number']}"
                            
                    #           if "make_static_image" in static_image:
                    #               fig = make_static_img(data.df_V.T,zmin = fzmin, zmax = fzmax, title = title,colorscale=colorscale)
                    #               if "tp_overlay" in overlay_tps:
                    #                   logging.info("TPs in V-Plane:")
                    #                   logging.info(data.tp_df_V)
                    #                   fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
                                    
                    #           else:
                    #               fig = px.imshow(data.df_V.T,  zmin=fzmin, zmax=fzmax,title=title, color_continuous_scale=colorscale,aspect='auto')
                    #               if "tp_overlay" in overlay_tps:
                    #                   logging.info("TPs in V-Plane:")
                    #                   logging.info(data.tp_df_V)
                    #                   fig.add_trace(tp_for_adc(data.tp_df_V, fzmin,fzmax))
                    #               fig.update_layout(
                                        
                    #                   height=600,yaxis_title="Offline Channel",
                    #                   xaxis_title="Time ticks",showlegend=True
                    #               )
                
                    #   add_dunedaq_annotation(fig)
                    #   fig.update_layout(font_family="Lato", title_font_family="Lato")
                    #   children += [html.B(f"ADC Counts: V-plane, Initial TS: {str(trigger_record_data(engine,trigger_record,raw_data_file).ts_min)}"),
                    #       dcc.Graph(figure=fig,style={"marginTop":"10px","marginBottom":"10px"}),
                    #   ]
                    #   fig.update_layout(legend=dict(yanchor="top", y=0.01, xanchor="left", x=1))
                    # if 'U' in adcmap_selection:
                    #   logging.info("U Plane selected")
                    #   """if "cnr_removal" in cnr:
                    #       rich.print("CNR selected")
                    #       rich.print("Raw ADCs in U-Plane after CNR:")
                    #       rich.print(data.df_cnr[data.planes.get(0, {})].T)
                            
                    #       title = f"U-plane (CNR): Run {data.info['run_number']}: {data.info['trigger_number']}"

                    #       if "make_static_image" in static_image:
                    #           fig = make_static_img(data.df_cnr[data.planes.get(0, {})].T, zmin = fzmin, zmax = fzmax, title = title)
                    #           if "tp_overlay" in overlay_tps:
                    #               rich.print("TPs in U-Plane:")
                    #               rich.print(data.tp_df_U)
                    #               fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
                    #       else:
                    #           fig = px.imshow(data.df_cnr[data.planes.get(0, {})].T, zmin=fzmin, zmax=fzmax, title=title, color_continuous_scale='plasma',aspect='auto')
                    #           if "tp_overlay" in overlay_tps:
                    #               rich.print("TPs in U-Plane:")
                    #               rich.print(data.tp_df_U)
                    #               fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
                    #           fig.update_layout(
                                        
                    #                   height=600,yaxis_title="Offline Channel",
                    #                   xaxis_title="Time ticks",showlegend=True
                    #                   )
                    #   else:"""
                    #   if "offset_removal" in offset:
                    #           logging.info("Offset removal selected")
                    #           logging.info("Raw ADCs in U-Plane after offset removal:")
                    #           logging.info((data.df_U - data.df_U_mean).T)
                                
                    #           title = f"U-plane offset removal, Run {data.info['run_number']}: {data.info['trigger_number']}"
                    #           if "make_static_image" in static_image:
                    #               fig = make_static_img((data.df_U - data.df_U_mean).T, zmin = fzmin, zmax = fzmax,title=title,colorscale=colorscale)
                    #               if "tp_overlay" in overlay_tps:
                    #                   logging.info("TPs in U-Plane:")
                    #                   logging.info(data.tp_df_U)
                    #                   fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
                
                    #           else:
                    #               fig = px.imshow((data.df_U - data.df_U_mean).T, zmin=fzmin, zmax=fzmax, title=title,color_continuous_scale=colorscale,aspect="auto")
                    #               if "tp_overlay" in overlay_tps:
                    #                   logging.info("TPs in U-Plane:")
                    #                   logging.info(data.tp_df_U)
                    #                   fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
                    #               fig.update_layout(
                                    
                    #                   height=600,yaxis_title="Offline Channel",
                    #                   xaxis_title="Time ticks",showlegend=True
                    #                   )

                    #   else:
                    #           logging.info("Raw ADCs in U-Plane:")
                    #           logging.info(data.df_U)
                                
                    #           title = f"U-plane, Run {data.info['run_number']}: {data.info['trigger_number']}"
                            
                    #           if "make_static_image" in static_image:
                    #               fig = make_static_img(data.df_U.T,zmin = fzmin, zmax = fzmax, title = title,colorscale=colorscale)
                    #               if "tp_overlay" in overlay_tps:
                    #                   logging.info("TPs in U-Plane:")
                    #                   logging.info(data.tp_df_U)
                    #                   fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
                                    
                    #           else:
                    #               fig = px.imshow(data.df_U.T, zmin=fzmin, zmax=fzmax, title=title, color_continuous_scale=colorscale,aspect='auto')
                    #               if "tp_overlay" in overlay_tps:
                    #                   logging.info("TPs in U-Plane:")
                    #                   logging.info(data.tp_df_U)
                    #                   fig.add_trace(tp_for_adc(data.tp_df_U, fzmin,fzmax))
                    #               fig.update_layout(
                                    
                    #                   height=600,yaxis_title="Offline Channel",
                    #                   xaxis_title="Time ticks",showlegend=True
                    #               )
                    #   add_dunedaq_annotation(fig)
                    #   fig.update_layout(font_family="Lato", title_font_family="Lato")
                    #   children += [html.B(f"ADC Counts: U-plane, Initial TS: {str(trigger_record_data(engine,trigger_record,raw_data_file).ts_min)}"),
                    #       dcc.Graph(figure=fig,style={"marginTop":"10px","marginBottom":"10px"}),
                    #   ]
                    #   fig.update_layout(legend=dict(yanchor="top", y=0.01, xanchor="left", x=1))
                    if adcmap_selection:
                        return(html.Div([
                            selection_line(partition,run,raw_data_file, trigger_record),
                            #html.Hr(),
                            html.Div(children)]))
                    else:
                        return(html.Div(html.H6("No ADC map selected")))
                    
                else:
                    return(html.Div(html.H6(nothing_to_plot())))
            return(original_state)
        return(html.Div())
