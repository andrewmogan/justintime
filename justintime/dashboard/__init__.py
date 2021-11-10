import dash
from .layout import generate
from .callbacks import attach

def init_app(engine):
    app = dash.Dash(
        __name__,
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    )
    app.title = "DUNE Prompt Feedback Dashboard"

    server = app.server
    app.config.suppress_callback_exceptions = True

    app.layout = generate(engine)
    attach(app, engine)
    return app