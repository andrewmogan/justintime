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
import datetime

from ..cruncher.signal import butter_highpass_filter

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
        logging.debug(f"Updatd file list: {fl}")
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
        logging.debug(f'data file: {raw_data_file}')

        if not raw_data_file:
            return []
        tr_nums = [{'label':str(n), 'value':str(n)} for n in brain.get_trigger_record_list(raw_data_file)]
        logging.debug(f'Trigger nums: {tr_nums}')
        return tr_nums


    @app.callback(
        Output('trigger-record-select-B', 'options'),
        Input('raw-data-file-select-B', 'value')
        )
    def update_trigger_record_select(raw_data_file):
        logging.debug(f'data file: {raw_data_file}')

        if not raw_data_file:
            return []
        tr_nums = [{'label':str(n), 'value':str(n)} for n in brain.get_trigger_record_list(raw_data_file)]
        logging.debug(f'Trigger nums: {tr_nums}')
        return tr_nums


    def calc_mean_std_by_plane(df, planes):
        df_std = df.std()
        df_mean = df.mean()
        logging.debug(f"Mean and standard deviation calculated")

        df_p0_mean = df_mean[planes[0]]
        df_p1_mean = df_mean[planes[1]]
        df_p2_mean = df_mean[planes[2]]

        df_p0_std = df_std[planes[0]]
        df_p1_std = df_std[planes[1]]
        df_p2_std = df_std[planes[2]]

        return (df_std, df_mean, df_p0_mean, df_p1_mean, df_p2_mean, df_p0_std, df_p1_std, df_p2_std)


    def calc_fft(df, planes):
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

        return df_fft2.sort_index()

    def calc_diffs(df_a, df_b, planes):
        # value_offset=4096
        dt_a_rst = df_a.reset_index().drop('ts', axis=1)
        dt_b_rst = df_b.reset_index().drop('ts', axis=1)
        dt_ab_diff = (dt_a_rst.astype('int')-dt_b_rst.astype('int'))

        return (dt_ab_diff[planes[0]], dt_ab_diff[planes[1]], dt_ab_diff[planes[2]])

    @app.callback(
        Output('mean_std_by_plane_card', 'children'),
        Input('plot_button', 'n_clicks'),
        State('raw-data-file-select-A', 'value'),
        State('trigger-record-select-A', 'value'),
        State('raw-data-file-select-B', 'value'),
        State('trigger-record-select-B', 'value'),
        State('plot_selection', 'value'),
        State('adcmap-selection-a', 'value'),
        State('adcmap-selection-b', 'value'),
        State('adcmap-selection-ab-diff', 'value'),
        State('adcmap-selection-a-filt', 'value'),
        State('adcmap-selection-a-filt-x', 'value'),
        State('ab-diff-range-slider', 'value'),
        )
    def update_plots(
        n_clicks,
        raw_data_file_a,
        trig_rec_num_a,
        raw_data_file_b,
        trig_rec_num_b,
        plot_selection,
        adcmap_selection_a,
        adcmap_selection_b,
        adcmap_selection_ab_diff,
        adcmap_selection_a_filt,
        adcmap_selection_a_filt_x,
        ab_diff_range
        ):
        # ctx = dash.callback_context

        children = []

        if not trig_rec_num_a or not trig_rec_num_b:
            raise PreventUpdate
        # #----
        info_a, df_a = brain.load_trigger_record(raw_data_file_a, int(trig_rec_num_a))
        logging.debug(f"Trigger record {trig_rec_num_a} from {raw_data_file_a} loaded")

        # #----
        info_b, df_b = brain.load_trigger_record(raw_data_file_b, int(trig_rec_num_b))
        logging.debug(f"Trigger record {trig_rec_num_b} from {raw_data_file_b} loaded")

        # Timestamp information
        ts_a = info_a['trigger_timestamp']*20/1000000000
        ts_b = info_b['trigger_timestamp']*20/1000000000

        dt_a = datetime.datetime.fromtimestamp(ts_a).strftime('%c')
        dt_b = datetime.datetime.fromtimestamp(ts_b).strftime('%c')

        # Group channel by plane
        group_planes = groupby(range(0,3200), lambda ch: brain.ch_map.get_plane_from_offline_channel(int(ch)))
        planes = {k: [x for x in d] for k,d in group_planes}
        rich.print(planes)


        df_a_std, df_a_mean, df_a_p0_mean, df_a_p1_mean, df_a_p2_mean, df_a_p0_std, df_a_p1_std, df_a_p2_std = calc_mean_std_by_plane(df_a, planes)
        df_b_std, df_b_mean, df_b_p0_mean, df_b_p1_mean, df_b_p2_mean, df_b_p0_std, df_b_p1_std, df_b_p2_std = calc_mean_std_by_plane(df_b, planes)


        if 'Mean_STD' in plot_selection:

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

            children += [
                    html.B("Mean by plane"),
                    html.Hr(),
                    dcc.Graph(figure=fig_mean),
                    html.B("STD by plane"),
                    html.Hr(),
                    dcc.Graph(figure=fig_std),
            ]

        if 'FFT' in plot_selection:

            df_a_fft2 = calc_fft(df_a, planes)
            df_b_fft2 = calc_fft(df_b, planes)

            df_U_plane = pd.concat([df_a_fft2['U-plane'], df_b_fft2['U-plane']], axis=1, keys=["A", "B"])
            df_V_plane = pd.concat([df_a_fft2['V-plane'], df_b_fft2['V-plane']], axis=1, keys=["A", "B"])
            df_Z_plane = pd.concat([df_a_fft2['Z-plane'], df_b_fft2['Z-plane']], axis=1, keys=["A", "B"])

            logging.debug(f"FFT plots created")

            children += [
                html.B("FFT U-Plane"),
                html.Hr(),
                dcc.Graph(figure=px.line(df_U_plane, log_y=True)),
                html.B("FFT V-Plane"),
                html.Hr(),
                dcc.Graph(figure=px.line(df_V_plane, log_y=True)),
                html.B("FFT Z-Plane"),
                html.Hr(),
                dcc.Graph(figure=px.line(df_Z_plane, log_y=True)),
            ]
        #----

        fig_w, fig_h = 1500, 1000
        # Waveforms A
        if 'Z' in adcmap_selection_a:
            fig = px.imshow(df_a[planes[2]], title=f"Z-plane, A - A: Run {info_a['run_number']}: {info_a['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map Z-plane"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'V' in adcmap_selection_a:
            fig = px.imshow(df_a[planes[1]], title=f"V-plane, A - A: Run {info_a['run_number']}: {info_a['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map V-plane"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'U' in adcmap_selection_a:
            fig = px.imshow(df_a[planes[0]], title=f"U-plane, A - A: Run {info_a['run_number']}: {info_a['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map U-plane"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]


        # Waveforms B
        if 'Z' in adcmap_selection_b:
            fig = px.imshow(df_b[planes[2]], title=f"Z-plane, B - B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map Z-plane"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'V' in adcmap_selection_b:
            fig = px.imshow(df_b[planes[1]], title=f"V-plane, B - B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map V-plane"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'U' in adcmap_selection_b:
            fig = px.imshow(df_b[planes[0]], title=f"U-plane, B - B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map U-plane"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        dt_ab_U_diff, dt_ab_V_diff, dt_ab_Z_diff = calc_diffs(df_a, df_b, planes)

        if 'Z' in adcmap_selection_ab_diff:
            fig = px.imshow(dt_ab_Z_diff, title=f"Z-plane, A-B - A: Run {info_a['run_number']}: {info_a['trigger_number']}, B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map Z-plane A-B"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'V' in adcmap_selection_ab_diff:
            fig = px.imshow(dt_ab_V_diff, title=f"V-plane, A-B - A: Run {info_a['run_number']}: {info_a['trigger_number']}, B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map V-plane A-B"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'U' in adcmap_selection_ab_diff:
            fig = px.imshow(dt_ab_U_diff, title=f"U-plane, A-B - A: Run {info_a['run_number']}: {info_a['trigger_number']}, B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map U-plane A-B"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        fps=2000000
        cutoff = 25000
        df_ab_U_filt = butter_highpass_filter(dt_ab_U_diff, cutoff, fps)
        df_ab_V_filt = butter_highpass_filter(dt_ab_V_diff, cutoff, fps)
        df_ab_Z_filt = butter_highpass_filter(dt_ab_Z_diff, cutoff, fps)


        fzmin, fzmax = ab_diff_range
        if 'Z' in adcmap_selection_a_filt:
            fig = px.imshow(df_ab_Z_filt, zmin=fzmin, zmax=fzmax, title=f"Z-plane, A-B (filtered) - A: Run {info_a['run_number']}: {info_a['trigger_number']}, B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map Z-plane A-B"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'V' in adcmap_selection_a_filt:
            fig = px.imshow(df_ab_V_filt, zmin=fzmin, zmax=fzmax, title=f"V-plane, A-B (filtered) - A: Run {info_a['run_number']}: {info_a['trigger_number']}, B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map V-plane A-B"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'U' in adcmap_selection_a_filt:
            fig = px.imshow(df_ab_U_filt, zmin=fzmin, zmax=fzmax, title=f"U-plane, A-B (filtered) - A: Run {info_a['run_number']}: {info_a['trigger_number']}, B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map U-plane A-B"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]



        # 
        crate_no = 4 # Randomish number
        offchan_to_hw = {}
        for slot_no in range(4):
            for fiber_no in range(1,3):
                for c in range(256):
                    off_ch = brain.ch_map.get_offline_channel_from_crate_slot_fiber_chan(crate_no, slot_no, fiber_no, c)
                    # offchan_to_hw[off_ch] = (crate_no, slot_no, fiber_no, c)
                    if off_ch == 4294967295:
                        continue
                    offchan_to_hw[off_ch] = (crate_no, slot_no, fiber_no, c)

        def femb_id_from_off(off_ch):
            # off_ch_str = str(off_ch)
            crate, slot, link, ch = offchan_to_hw[off_ch]
            # return off_femb_map[ch_str][:3]+[off_femb_map[ch_str][3]//128]
            return 4*slot+2*(link-1)+ch//128 

        # group_fembs = groupby(offchan_to_hw, femb_id_from_off)
        # fembs = {k: [int(x) for x in d] for k,d in group_fembs}
        femb_to_chans = {k: [int(x) for x in d] for k,d in groupby(offchan_to_hw, femb_id_from_off)}
        df_sub = df_a.copy()
        for p in planes:
            for f in femb_to_chans:
                chans = list(set(planes[p]) & set(femb_to_chans[f]))
                df_sub[chans] = df_sub[chans].sub(df_sub[chans].mean(axis=1), axis=0)

        fzmin, fzmax = ab_diff_range
        if 'Z' in adcmap_selection_a_filt_x:
            fig = px.imshow(df_sub[planes[2]]-df_sub[planes[2]].mean(), zmin=fzmin, zmax=fzmax, title=f"Z-plane, A-B (filtered - X) - A: Run {info_a['run_number']}: {info_a['trigger_number']}, B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map Z-plane A-B"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'V' in adcmap_selection_a_filt_x:
            fig = px.imshow(df_sub[planes[1]]-df_sub[planes[1]].mean(), zmin=fzmin, zmax=fzmax, title=f"V-plane, A-B (filtered - X) - A: Run {info_a['run_number']}: {info_a['trigger_number']}, B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map V-plane A-B"),
                html.Hr(),
                dcc.Graph(figure=fig),
            ]

        if 'U' in adcmap_selection_a_filt_x:
            fig = px.imshow(df_sub[planes[0]]-df_sub[planes[0]].mean(), zmin=fzmin, zmax=fzmax, title=f"U-plane, A-B (filtered - X) - A: Run {info_a['run_number']}: {info_a['trigger_number']}, B: Run {info_b['run_number']}: {info_b['trigger_number']}", aspect='auto')
            fig.update_layout(
                width=fig_w,
                height=fig_h,
            )
            children += [
                html.B("Heat map U-plane A-B"),
                html.Hr(),
                dcc.Graph(figure=fig),
                ]

        return [
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H4(f"Trigger Record A"),
                                html.H2(f"Run: {info_a['run_number']} Trigger: {info_a['trigger_number']}"),
                                html.H5(f"{dt_a}"),
                                html.H6(f"{raw_data_file_a}"),
                                ], 
                            style={'display': 'inline-block', 'width': '50%'}
                        ),
                        html.Div(
                            children=[
                                html.H4(f"Trigger Record B"),
                                html.H2(f"Run: {info_b['run_number']} Trigger: {info_b['trigger_number']}"),
                                html.H5(f"{dt_b}"),
                                html.H6(f"{raw_data_file_b}"),
                            ],
                            style={'display': 'inline-block', 'width': '50%'}
                        ),
                    ]
                ),
                ] + children

        
