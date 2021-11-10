from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from dash import html

from .layout import generate_file_wizard


def register(app):
    @app.callback(
        Output("sidebar", "className"),
        Input("sidebar-toggle", "n_clicks"),
        State("sidebar", "className"),
        )
    def toggle_classname(n, classname):
        if n and classname == "":
            return "collapsed"
        return ""

    @app.callback(
        Output("collapse", "is_open"),
        Input("navbar-toggle", "n_clicks"),
        State("collapse", "is_open"),
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("page-content", "children"),
        Input("main-control", "active_item")
        )
    def render_page_content(active_item):
        print(active_item)
        if active_item == "item_file_wizard":
            return [html.Div(generate_file_wizard())]
        elif active_item == "item_tr_inspector":
            return [html.Div(html.P(active_item))]
        elif active_item == "item_noise_view":
            return [html.Div(html.P(active_item))]
        else:
            raise PreventUpdate

# # Callback: page selection
# @app.callback(
#     [Output("page-content", "children"),
#      Output("interval-content-refresher", "disabled")
#     ],
#     [Input("url", "pathname"),
#      Input("interval-content-refresher", "n_intervals")
#     ],
#     )
# def render_page_content(pathname, n):
#     if pathname in ["/", "/page-1"]:
#         if clIT.analyzer.country_ready:
#             return html.Div([
#                 html.H5('Daily')
#             ]+
#             [
#                 dcc.Graph(figure=f, style={'height':'50vh'}) for n,f in clIT.analyzer.figs_country_daily.items()
#             ]+[
#                 html.H5('Weekly')
#             ]+
#             [
#                 dcc.Graph(figure=f, style={'height':'50vh'}) for n,f in clIT.analyzer.figs_country_weekly.items()
#             ]), True
            
#         else:
#             return html.Div([
#                 html.H5("Stand by, loading data, plotting plots..."),
#             ]), False

#     elif pathname == "/page-2":
#         if clIT.analyzer.regs_ready:
#             return html.Div([
#                 dcc.Graph(figure=f) for n,f in clIT.analyzer.figs_regs_cumul.items()
#             ]), True
            
#         else:
#             return html.Div([
#                 html.H5("Stand by, loading data, plotting plots..."),
#             ]), False


#     elif pathname == "/page-3":
#         if clIT.analyzer.regs_ready:
#             return html.Div([
#                 dcc.Graph(figure=f) for n,f in clIT.analyzer.figs_regs_diff.items()
#             ]), True
#         else:
#             return html.Div([
#                 html.H5("Stand by, loading data, plotting plots..."),
#             ]), False

#     elif pathname == "/page-4":
#         if clIT.analyzer.regs_ready:
#             return html.Div([
#                 dcc.Graph(figure=f) for n,f in clIT.analyzer.figs_regs_roll5.items()
#             ]), True
#         else:
#             return html.Div([
#                 html.H5("Stand by, loading data, plotting plots..."),
#             ]), False

#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     ), True