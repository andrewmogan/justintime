from dash import html, dcc
from dash.dependencies import Input, Output, State
import logging
from .. import ctrl_class

def return_obj(dash_app, engine):
    ctrl_id = "03_refresh_ctrl"
    data=engine.get_session_run_files_map()
    ctrl_div = html.Div([html.Button('Refresh Files', id=ctrl_id, n_clicks=0)])
    ctrl = ctrl_class.ctrl("refresh_button", ctrl_id, ctrl_div, engine)
    init_callbacks(dash_app, engine,data)
    return(ctrl)
    
def init_callbacks(dash_app, engine,data):
    
    @dash_app.callback(
		Output('partition_select_ctrl', 'options'),
		Input('03_refresh_ctrl', 'n_clicks'))
        
    def update_file_list(n_clicks):
        data=engine.get_session_run_files_map()
        opts = list(data.keys())
        return (opts)