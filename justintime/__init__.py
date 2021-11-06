import dash
from .layout import generate

class JITDash(dash.Dash):
    """

    """
    def __init__(self, name=None, server=True, assets_folder='assets', assets_url_path='assets', assets_ignore='', assets_external_path=None, include_assets_files=True, url_base_pathname=None, requests_pathname_prefix=None, routes_pathname_prefix=None, serve_locally=True, compress=True, meta_tags=None, index_string=..., external_scripts=None, external_stylesheets=None, suppress_callback_exceptions=None, show_undo_redo=False, plugins=None, **obsolete):
        super().__init__(name=name, server=server, assets_folder=assets_folder, assets_url_path=assets_url_path, assets_ignore=assets_ignore, assets_external_path=assets_external_path, include_assets_files=include_assets_files, url_base_pathname=url_base_pathname, requests_pathname_prefix=requests_pathname_prefix, routes_pathname_prefix=routes_pathname_prefix, serve_locally=serve_locally, compress=compress, meta_tags=meta_tags, index_string=index_string, external_scripts=external_scripts, external_stylesheets=external_stylesheets, suppress_callback_exceptions=suppress_callback_exceptions, show_undo_redo=show_undo_redo, plugins=plugins, **obsolete)


app = JITDash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "DUNE Promt Feedback Dashboard"

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = generate()