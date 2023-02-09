import dash_bootstrap_components as dbc
import load_all as ld
from dash import Dash, html, dcc, callback_context
from dash.dependencies import Input, Output, State
import load_all as ld
from cruncher.datamanager import DataManager
import dash_bootstrap_components as dbc
import click
import rich

def create_navbar(pages):

    # Create the Navbar using Dash Bootstrap Components
    navbar = dbc.NavbarSimple(style={'fontSize': '20px ',},
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu", # Label given to the dropdown menu
                color="white",
                
                children=[
                    # In this part of the code we create the items that will appear in the dropdown menu on the right
                    # side of the Navbar.  The first parameter is the text that appears and the second parameter 
                    # is the URL extension.
                    dbc.DropdownMenuItem("Home", href='/',style={'fontSize': '14px '}), # Hyperlink item that appears in the dropdown menu
                    html.Div([dbc.DropdownMenuItem(page.name, href=f"/{page.id}") for page in pages],style={'fontSize': '14px '}),
   
        ] 
            ),
        ],
        brand="Home",  # Set the text on the left side of the Navbar
        brand_href="/",  # Set the URL where the user will be sent when they click the brand we just created "Home"
        sticky="top",  # Stick it to the top... like Spider Man crawling on the ceiling?
        color="primary",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for light text)
        
    )
    return navbar