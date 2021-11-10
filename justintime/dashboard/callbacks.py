import dash
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd

import logging
from itertools import groupby

def attach(app: Dash, brain) -> None:
    
    @app.callback(
        Output('trigger-record-select', 'options'),
        Input('raw-data-file-select', 'value')
        )
    def update_trigger_record_select(raw_data_file):
        logging.info(f'data file: {raw_data_file}')

        if not raw_data_file:
            return []
        tr_nums = [{'label':str(n), 'value':str(n)} for n in brain.get_trigger_record_list(raw_data_file)]
        logging.info(f'Trigger nums: {tr_nums}')
        return tr_nums

    @app.callback(
        Output('mean_std_by_plane_card', 'children'),
        Input('raw-data-file-select', 'value'),
        Input('trigger-record-select', 'value')
        )
    def update_mean_std_by_plane(raw_data_file, trig_rec_num):
        ctx = dash.callback_context

        input_src_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if input_src_id != 'trigger-record-select':
            raise PreventUpdate

        #----
        df = brain.load_trigger_record(raw_data_file, int(trig_rec_num))
        logging.debug(f"Trigger record {trig_rec_num} from {raw_data_file} loaded")
        df_std = df.std()
        df_mean = df.mean()
        logging.debug(f"Mean and standard deviation calculated")

        # Group channel by plane
        group_planes = groupby(df.columns, lambda ch: brain.ch_map.get_plane_from_offline_channel(int(ch)))
        planes = {k: [x for x in d] for k,d in group_planes}
        
        df_p0_mean = df_mean[planes[0]]
        df_p1_mean = df_mean[planes[1]]
        df_p2_mean = df_mean[planes[2]]

        df_p0_std = df_std[planes[0]]
        df_p1_std = df_std[planes[1]]
        df_p2_std = df_std[planes[2]]

        fig_mean = make_subplots(rows=1, cols=3,
                            subplot_titles=("Mean U-Plane", "Mean V-Plane", "Mean Z-Plane"))
        fig_mean.add_trace(
            go.Scattergl(x=df_p0_mean.index.astype(int), y=df_p0_mean, mode='markers'),
            row=1, col=1
        )
        fig_mean.add_trace(
            go.Scattergl(x=df_p1_mean.index.astype(int), y=df_p1_mean, mode='markers'),
            row=1, col=2
        )
        fig_mean.add_trace(
            go.Scattergl(x=df_p2_mean.index.astype(int), y=df_p2_mean, mode='markers'),
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
            showlegend=False
        )

        logging.debug(f"Mean plots created")


        fig_std = make_subplots(rows=1, cols=3,
                            subplot_titles=("STD U-Plane", "STD V-Plane", "STD Z-Plane"))
        fig_std.add_trace(
            go.Scattergl(x=df_p0_std.index.astype(int), y=df_p0_std, mode='markers'),
            row=1, col=1
        )
        fig_std.add_trace(
            go.Scattergl(x=df_p1_std.index.astype(int), y=df_p1_std, mode='markers'),
            row=1, col=2
        )
        fig_std.add_trace(
            go.Scattergl(x=df_p2_std.index.astype(int), y=df_p2_std, mode='markers'),
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
            showlegend=False
        )

        logging.debug(f"STD plots created")



        #----
        df_sum_U = df[planes[0]].sum(axis=1).to_frame()
        df_sum_U = df_sum_U.rename(columns= {0: 'U-plane'})
        df_sum_V = df[planes[1]].sum(axis=1).to_frame()
        df_sum_V = df_sum_V.rename(columns= {0: 'V-plane'})
        df_sum_Z = df[planes[2]].sum(axis=1).to_frame()
        df_sum_Z = df_sum_Z.rename(columns= {0: 'Z-plane'})
        df_sums = pd.concat([df_sum_U, df_sum_V, df_sum_Z], axis=1)


        df_fft = df_sums.apply(np.fft.fft)
        df_fft2 = np.abs(df_fft) ** 2
        freq = np.fft.fftfreq(8192, 0.5e-6)
        df_fft2['Freq'] = freq
        df_fft2 = df_fft2[df_fft2['Freq']>0]
        df_fft2 = df_fft2.set_index('Freq')
        fig_fft = px.line(df_fft2.sort_index())

        logging.debug(f"FFT plots created")

        #----

        fig_hm_p0 = px.imshow(df[planes[0]])
        fig_hm_p1 = px.imshow(df[planes[1]])
        fig_hm_p2 = px.imshow(df[planes[2]])

        # def df_to_plotly(df):
        #     return {'z': df.values.tolist(),
        #             'x': df.columns.tolist(),
        #             'y': df.index.tolist()}

        # fig_hm_p0 = go.Figure(data=go.Heatmapgl(df_to_plotly(df[planes[0]])))
        # fig_hm_p1 = go.Figure(data=go.Heatmapgl(df_to_plotly(df[planes[1]])))
        # fig_hm_p2 = go.Figure(data=go.Heatmapgl(df_to_plotly(df[planes[2]])))

        logging.debug(f"Heatmaps created")

        return [
                html.B("Mean by plane"),
                html.Hr(),
                dcc.Graph(figure=fig_mean),
                html.B("STD by plane"),
                html.Hr(),
                dcc.Graph(figure=fig_std),
                html.B("FFT by plane"),
                html.Hr(),
                dcc.Graph(figure=fig_fft),
                html.B("Heat map U-plane"),
                html.Hr(),
                dcc.Graph(figure=fig_hm_p0),
                html.B("Heat map V-plane"),
                html.Hr(),
                dcc.Graph(figure=fig_hm_p1),
                html.B("Heat map Z-plane"),
                html.Hr(),
                dcc.Graph(figure=fig_hm_p2),
            ]
