import dash
import dash_bootstrap_components as dbc

from . import layout
from . import callbacks

def init_app():
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.CYBORG],
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    )
    app.title = "DUNE Prompt Feedback Dashboard"

    server = app.server
    app.config.suppress_callback_exceptions = True

    app.layout = layout.generate()
    callbacks.register(app)
    return app