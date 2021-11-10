import dash
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd

import logging
from itertools import groupby
import rich

def attach(app: Dash, brain) -> None:

    @app.callback(
        Output('raw-data-file-select-A', 'options'),
        Output('raw-data-file-select-B', 'options'),
        Input('refresh_files', 'n_clicks')      
        )
    def update_file_list(pathname):
        fl = sorted(brain.list_files(), reverse=True)
        rich.print(f"Updatd file list: {fl}")
        opts = [{'label': f, 'value':f} for f in sorted(brain.list_files(), reverse=True)]
        return (
            opts,
            opts
            )


    @app.callback(
        Output('trigger-record-select-A', 'options'),
        Input('raw-data-file-select-A', 'value')
        )
    def update_trigger_record_select(raw_data_file):
        logging.info(f'data file: {raw_data_file}')

        if not raw_data_file:
            return []
        tr_nums = [{'label':str(n), 'value':str(n)} for n in brain.get_trigger_record_list(raw_data_file)]
        logging.info(f'Trigger nums: {tr_nums}')
        return tr_nums


    @app.callback(
        Output('trigger-record-select-B', 'options'),
        Input('raw-data-file-select-B', 'value')
        )
    def update_trigger_record_select(raw_data_file):
        logging.info(f'data file: {raw_data_file}')

        if not raw_data_file:
            return []
        tr_nums = [{'label':str(n), 'value':str(n)} for n in brain.get_trigger_record_list(raw_data_file)]
        logging.info(f'Trigger nums: {tr_nums}')
        return tr_nums


    def mean_std_by_plane(df, ch_map):
        df_std = df.std()
        df_mean = df.mean()
        logging.debug(f"Mean and standard deviation calculated")

        # Group channel by plane
        group_planes_a = groupby(df.columns, lambda ch: ch_map.get_plane_from_offline_channel(int(ch)))
        planes_a = {k: [x for x in d] for k,d in group_planes_a}
        
        df_p0_mean = df_mean[planes_a[0]]
        df_p1_mean = df_mean[planes_a[1]]
        df_p2_mean = df_mean[planes_a[2]]

        df_p0_std = df_std[planes_a[0]]
        df_p1_std = df_std[planes_a[1]]
        df_p2_std = df_std[planes_a[2]]

        return (df_std, df_mean, df_p0_mean, df_p1_mean, df_p2_mean, df_p0_std, df_p1_std, df_p2_std)



    @app.callback(
        Output('mean_std_by_plane_card', 'children'),
        Input('plot_button', 'n_clicks'),
        State('raw-data-file-select-A', 'value'),
        State('trigger-record-select-A', 'value'),
        State('raw-data-file-select-B', 'value'),
        State('trigger-record-select-B', 'value')
        )
    def update_mean_std_by_plane(n_clicks, raw_data_file_a, trig_rec_num_a, raw_data_file_b, trig_rec_num_b):
        ctx = dash.callback_context

        if not trig_rec_num_a or not trig_rec_num_b:
            raise PreventUpdate
        # #----
        info_a, df_a = brain.load_trigger_record(raw_data_file_a, int(trig_rec_num_a))
        logging.debug(f"Trigger record {trig_rec_num_a} from {raw_data_file_a} loaded")

        # #----
        info_b, df_b = brain.load_trigger_record(raw_data_file_b, int(trig_rec_num_b))
        logging.debug(f"Trigger record {trig_rec_num_b} from {raw_data_file_b} loaded")

        df_a_std, df_a_mean, df_a_p0_mean, df_a_p1_mean, df_a_p2_mean, df_a_p0_std, df_a_p1_std, df_a_p2_std = mean_std_by_plane(df_a, brain.ch_map)
        df_b_std, df_b_mean, df_b_p0_mean, df_b_p1_mean, df_b_p2_mean, df_b_p0_std, df_b_p1_std, df_b_p2_std = mean_std_by_plane(df_b, brain.ch_map)



        fig_mean = make_subplots(rows=1, cols=3,
                            subplot_titles=("Mean U-Plane", "Mean V-Plane", "Mean Z-Plane"))
        fig_mean.add_trace(
            go.Scattergl(x=df_a_p0_mean.index.astype(int), y=df_a_p0_mean, mode='markers', name=f"Run {info_a['run_number']}: {info_a['trigger_number']}"),
            row=1, col=1
        )
        fig_mean.add_trace(
            go.Scattergl(x=df_b_p0_mean.index.astype(int), y=df_b_p0_mean, mode='markers', name=f"Run {info_b['run_number']}: {info_b['trigger_number']}"),
            row=1, col=1
        )

        fig_mean.add_trace(
            go.Scattergl(x=df_a_p1_mean.index.astype(int), y=df_a_p1_mean, mode='markers', name=f"Run {info_a['run_number']}: {info_a['trigger_number']}"),
            row=1, col=2
        )
        fig_mean.add_trace(
            go.Scattergl(x=df_b_p1_mean.index.astype(int), y=df_b_p1_mean, mode='markers', name=f"Run {info_b['run_number']}: {info_b['trigger_number']}"),
            row=1, col=2
        )


        fig_mean.add_trace(
            go.Scattergl(x=df_a_p2_mean.index.astype(int), y=df_a_p2_mean, mode='markers', name=f"Run {info_a['run_number']}: {info_a['trigger_number']}"),
            row=1, col=3
        )
        fig_mean.add_trace(
            go.Scattergl(x=df_b_p2_mean.index.astype(int), y=df_b_p2_mean, mode='markers', name=f"Run {info_b['run_number']}: {info_b['trigger_number']}"),
            row=1, col=3
        )


        fig_mean.update_layout(
            # autosize=False,
            # width=1200,
            # height=600,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            ),
            # showlegend=False
        )

        logging.debug(f"Mean plots created")


        fig_std = make_subplots(rows=1, cols=3,
                            subplot_titles=("STD U-Plane", "STD V-Plane", "STD Z-Plane"))
        fig_std.add_trace(
            go.Scattergl(x=df_a_p0_std.index.astype(int), y=df_a_p0_std, mode='markers', name=f"Run {info_a['run_number']}: {info_a['trigger_number']}"),
            row=1, col=1
        )
        fig_std.add_trace(
            go.Scattergl(x=df_b_p0_std.index.astype(int), y=df_b_p0_std, mode='markers', name=f"Run {info_b['run_number']}: {info_b['trigger_number']}"),
            row=1, col=1
        )

        fig_std.add_trace(
            go.Scattergl(x=df_a_p1_std.index.astype(int), y=df_a_p1_std, mode='markers', name=f"Run {info_a['run_number']}: {info_a['trigger_number']}"),
            row=1, col=2
        )
        fig_std.add_trace(
            go.Scattergl(x=df_b_p1_std.index.astype(int), y=df_b_p1_std, mode='markers', name=f"Run {info_b['run_number']}: {info_b['trigger_number']}"),
            row=1, col=2
        )

        fig_std.add_trace(
            go.Scattergl(x=df_a_p2_std.index.astype(int), y=df_a_p2_std, mode='markers', name=f"Run {info_a['run_number']}: {info_a['trigger_number']}"),
            row=1, col=3
        )
        fig_std.add_trace(
            go.Scattergl(x=df_b_p2_std.index.astype(int), y=df_b_p2_std, mode='markers', name=f"Run {info_b['run_number']}: {info_b['trigger_number']}"),
            row=1, col=3
        )

        fig_std.update_layout(
            # autosize=False,
            # width=1200,
            # height=600,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            ),
            # showlegend=False
        )

        logging.debug(f"STD plots created")



        # #----
        # df_sum_U = df[planes[0]].sum(axis=1).to_frame()
        # df_sum_U = df_sum_U.rename(columns= {0: 'U-plane'})
        # df_sum_V = df[planes[1]].sum(axis=1).to_frame()
        # df_sum_V = df_sum_V.rename(columns= {0: 'V-plane'})
        # df_sum_Z = df[planes[2]].sum(axis=1).to_frame()
        # df_sum_Z = df_sum_Z.rename(columns= {0: 'Z-plane'})
        # df_sums = pd.concat([df_sum_U, df_sum_V, df_sum_Z], axis=1)


        # df_fft = df_sums.apply(np.fft.fft)
        # df_fft2 = np.abs(df_fft) ** 2
        # freq = np.fft.fftfreq(8192, 0.5e-6)
        # df_fft2['Freq'] = freq
        # df_fft2 = df_fft2[df_fft2['Freq']>0]
        # df_fft2 = df_fft2.set_index('Freq')
        # fig_fft = px.line(df_fft2.sort_index())

        # logging.debug(f"FFT plots created")

        #----

        # fig_hm_p0 = px.imshow(df[planes[0]])
        # fig_hm_p1 = px.imshow(df[planes[1]])
        # fig_hm_p2 = px.imshow(df[planes[2]])

        # # def df_to_plotly(df):
        # #     return {'z': df.values.tolist(),
        # #             'x': df.columns.tolist(),
        # #             'y': df.index.tolist()}

        # # fig_hm_p0 = go.Figure(data=go.Heatmapgl(df_to_plotly(df[planes[0]])))
        # # fig_hm_p1 = go.Figure(data=go.Heatmapgl(df_to_plotly(df[planes[1]])))
        # # fig_hm_p2 = go.Figure(data=go.Heatmapgl(df_to_plotly(df[planes[2]])))

        # logging.debug(f"Heatmaps created")

        import datetime

        ts_a = info_a['trigger_timestamp']*20/1000000000
        ts_b = info_b['trigger_timestamp']*20/1000000000

        dt_a = datetime.datetime.fromtimestamp(ts_a).strftime('%c')
        dt_b = datetime.datetime.fromtimestamp(ts_b).strftime('%c')
        # rich.print(f"{dt_a} {dt_b}")

        return [
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H4(f"Trigger Record A"),
                                html.H2(f"Run: {info_a['run_number']} Trigger: {info_a['trigger_number']}"),
                                html.H5(f"Timestamp {dt_a}"),
                                ], 
                            style={'display': 'inline-block', 'width': '50%'}
                        ),
                        html.Div(
                            children=[
                                html.H4(f"Trigger Record B"),
                                html.H2(f"Run: {info_b['run_number']} Trigger: {info_b['trigger_number']}"),
                                html.H5(f"Timestamp {dt_b}"),
                            ],
                            style={'display': 'inline-block', 'width': '50%'}
                        ),
                    ]
                ),

                html.B("Mean by plane"),
                html.Hr(),
                dcc.Graph(figure=fig_mean),
                html.B("STD by plane"),
                html.Hr(),
                dcc.Graph(figure=fig_std),
                # html.B("FFT by plane"),
                # html.Hr(),
                # dcc.Graph(figure=fig_fft),
                # html.B("Heat map U-plane"),
                # html.Hr(),
                # dcc.Graph(figure=fig_hm_p0),
                # html.B("Heat map V-plane"),
                # html.Hr(),
                # dcc.Graph(figure=fig_hm_p1),
                # html.B("Heat map Z-plane"),
                # html.Hr(),
                # dcc.Graph(figure=fig_hm_p2),
            ]
