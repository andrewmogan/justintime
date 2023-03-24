from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import rich
import plotly.express as px
from .. import ctrl_class
from ... cruncher.datamanager import DataManager

def return_obj(dash_app, engine):
    ctrl_id = "20_orientation_height_ctrl"

    ctrl_div = html.Div(
        html.Div([
         
            html.Label("Select Orientation and Height: ",style={"fontSize":"12px"}),
            dbc.Row([
                dbc.Col(html.Div([
                    # dcc.Dropdown(options=list(data.keys()),placeholder="Partition",
                    dcc.Dropdown(options=["horizontal","vertical"],value='vertical',
            id="orientation_ctrl", clearable=False,
                       ),

                  
                 ],style={"marginBottom":"1.0em"})),

                dbc.Col(html.Div([
            
                    dcc.Input( type='number', min=500, max=5000, step=1,placeholder="Height",
                        id="height_select_ctrl",value=600,
                    ),
                    ],style={"marginBottom":"1.0em"}))
                ])],style={"marginTop":"1.0em","marginBottom":"0.2em"}),
        id=ctrl_id
    )
    

    ctrl = ctrl_class.ctrl("name2", ctrl_id, ctrl_div, engine)
    
   
    return(ctrl)