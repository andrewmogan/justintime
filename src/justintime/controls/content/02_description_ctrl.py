from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from .. import ctrl_class


def return_obj(dash_app, engine):
    
    ctrl_id = "02_description_ctrl"
    ctrl_div =   html.Div(
    [
        dbc.Button("Description", id="open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Page Information")),
                dbc.ModalBody(id="plot_description",style={"fontSize":"14px"}),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id=ctrl_id,
            is_open=False,
        ),
    ],style={"marginBottom":"1em","marginTop":"1em"}
)
    
    ctrl = ctrl_class.ctrl("description", ctrl_id, ctrl_div, engine)
   
    return(ctrl)

