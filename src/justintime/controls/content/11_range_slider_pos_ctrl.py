from dash import html, dcc
from dash.dependencies import Input, Output, State

from .. import ctrl_class

def return_obj(dash_app, engine):
    ctrl_id = "11_range_slider_pos_ctrl"
    comp_id = "11_range_slider_pos_comp"

    ctrl_div = html.Div([
        dcc.RangeSlider(
            id= comp_id,
            min=0,
            max=1024,
            step=64,
            value=[0, 192],
            marks={ v:f"{v}" for v in range(0, 1025, 256) },
            
        )
    ], id = ctrl_id)

    ctrl = ctrl_class.ctrl("range_slider", ctrl_id, ctrl_div, engine)

    return(ctrl)
