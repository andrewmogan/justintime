from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from .. import ctrl_class

def return_obj(dash_app, engine, storage):
    
    ctrl_id = "01_clickable_title_ctrl"
    
    ctrl_div=html.Div([
            html.H2(n_clicks=0,
            
            id=ctrl_id,
        ),
   
    ],style={
                #"textDecoration": "underline",
                "cursor": "pointer",
                
            },)
    ctrl = ctrl_class.ctrl("title", ctrl_id, ctrl_div, engine)
    ctrl.add_ctrl("02_description_ctrl")
    init_callbacks(dash_app, engine)
    return(ctrl)

def init_callbacks(dash_app, engine):
   
    @dash_app.callback(Output("02_description_ctrl", "is_open"),Input("01_clickable_title_ctrl", "n_clicks"), Input("close", "n_clicks"),[State("02_description_ctrl", "is_open")],)
    
    def toggle_modal(n1, n2, is_open):

        if n1 or n2:
            return not is_open
        return is_open