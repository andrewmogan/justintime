from dash import dcc
from dash import html

from dash import dash_table
import dash_bootstrap_components as dbc


def generate_sidebar():

    return html.Div(
        id="sidebar",
        children=[
            # Sidebar header
            dbc.Row(
                children=[
                    dbc.Col(html.H4("Just-in-Time")),
                    dbc.Col(
                        [
                            html.Button(
                                # use the Bootstrap navbar-toggler classes to style
                                html.Span(className="navbar-toggler-icon"),
                                className="navbar-toggler",
                                # the navbar-toggler classes don't set color
                                id="navbar-toggle",
                            ),
                            html.Button(
                                # use the Bootstrap navbar-toggler classes to style
                                html.Span(className="navbar-toggler-icon"),
                                className="navbar-toggler",
                                # the navbar-toggler classes don't set color
                                id="sidebar-toggle",
                            ),
                        ],
                        # the column containing the toggle will be only as wide as the
                        # toggle, resulting in the toggle being right aligned
                        width="auto",
                        # vertically align the toggle in the center
                        align="center",
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.P(
                        "(Proto)DUNE prompt-feedback",
                        className="lead",
                    ),
                    html.Hr(),
                ],
                id="blurb",
            ),
            # use the Collapse component to animate hiding / revealing links
            dbc.Collapse(
                id="collapse",
                children=[
                    dbc.Accordion(
                        id="main-control",
                        children=[
                            dbc.AccordionItem(
                                [
                                    html.P("Select Raw Data Files"),
                                ],
                                title="File Wizard",
                                item_id="item_file_wizard",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("This is the content of the second section"),
                                    dbc.Button("Don't click me!", color="danger"),
                                ],
                                title="TR Inspector",
                                item_id="item_tr_inspector",
                            ),
                            dbc.AccordionItem(
                                "This is the content of the third section",
                                title="Noise View",
                                item_id="item_noise_view",
                            ),
                        ],
                        flush=True,
                        start_collapsed=True,
                    )      
                ],
            ),
        ]
    )

def generate_splash():
    return html.Div(
        dbc.Container(
            [
                html.H1("DUNE Prompt Feedback", className="display-3"),
                html.P(
                    "Minimal plotting service to asses raw data quality just-in-time.",
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(
                    "Use utility classes for typography and spacing to suit the "
                    "larger container."
                ),
                html.P(
                    dbc.Button("Learn more", color="primary"), className="lead"
                ),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-light rounded-3",
    )

def generate():

    # loader_monitor = dcc.Interval(
    #             id='interval-data-loader-it',
    #             interval=1*1000, # in milliseconds
    #             n_intervals=0
    #         )

    # content_refresher = dcc.Interval(
    #                 id='interval-content-refresher',
    #                 interval=1*1000, # in milliseconds
    #                 n_intervals=0,
    #                 disabled=True
    #             )

    return html.Div(
        id="app-container",
        children = [
            # represents the URL bar, doesn't render anything
            dcc.Location(id='url', refresh=False),
            generate_sidebar(),
            html.Div(
                id="page-content",
                children=[
                    generate_splash()
                ]
            )
        ]
    )


# ----

def generate_file_wizard():
    table_header = [
        html.Thead(html.Tr([html.Th("File"), html.Th("Run"), html.Th("TRs")]))
    ]

    row1 = html.Tr([html.Td("a.hdf5"), html.Td("123"), html.Td()])
    row2 = html.Tr([html.Td("b.hdf5"), html.Td("456"), html.Td("")])

    table_body = [html.Tbody([row1, row2])]

    return dbc.Table(table_header + table_body, bordered=True)
