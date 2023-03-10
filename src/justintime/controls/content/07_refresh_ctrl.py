from dash import html, dcc
from dash.dependencies import Input, Output, State
import logging
from .. import ctrl_class

def return_obj(dash_app, engine):
    ctrl_id = "07_refresh_ctrl"
   
    ctrl_div = html.Div([html.Button('Refresh Files', id=ctrl_id, n_clicks=0)],style={"marginBottom":"1.0em"})
    ctrl = ctrl_class.ctrl("refresh_button", ctrl_id, ctrl_div, engine)
    
    init_callbacks(dash_app, engine)

    return(ctrl)
    
def init_callbacks(dash_app, engine):
    @dash_app.callback(
        Output('session_run_files_map', 'data'),
        Input('07_refresh_ctrl', 'n_clicks')
        )
    def update_file_list(n_clicks):  
        logging.debug('update files clicked!')
        data=engine.get_session_run_files_map()
        return (data)