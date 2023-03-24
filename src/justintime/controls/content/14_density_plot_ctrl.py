from dash import html, dcc
from dash.dependencies import Input, Output, State

from .. import ctrl_class

def return_obj(dash_app, engine):
    ctrl_id = "14_density_plot_ctrl"

    ctrl_div = html.Div([dcc.Checklist(options=["density_plot"], value = ["density_plot"],id=ctrl_id)],style={"fontSize": "1.5rem"})

    ctrl = ctrl_class.ctrl("density", ctrl_id, ctrl_div, engine)

    return(ctrl)
