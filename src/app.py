from dash import Dash, html, dcc, callback_context
from dash.dependencies import Input, Output, State
import load_all as ld
from cruncher.datamanager import DataManager
from navbar import create_navbar
#from header import create_header
from all_data import all_data_storage
from dash_bootstrap_templates import ThemeSwitchAIO,load_figure_template
import dash_bootstrap_components as dbc
import click
import rich
from PIL import Image


@click.command()
@click.option('-p', '--port', type=int, default=8001)
@click.argument('raw_data_path', type=click.Path(exists=True, file_okay=False))
@click.argument('channel_map_id', type=click.Choice(['VDColdbox', 'ProtoDUNESP1', 'PD2HD', 'VST']))
@click.argument('frame_type', type=click.Choice(['ProtoWIB', 'WIB']))
def main(raw_data_path :str, port: int, channel_map_id:str, frame_type: str):

	channel_map_id += 'ChannelMap'
	dash_app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
	##theme_switch = ThemeSwitchAIO(
    ##aio_id="theme", themes=[dbc.themes.DARKLY, dbc.themes.SUPERHERO]
	##)
	#templates=[dbc.themes.COSMO, dbc.themes.SUPERHERO]
	#load_figure_template(templates)
	##rich.print(theme_switch)
	init_dashboard(dash_app, raw_data_path, frame_type, channel_map_id)
	debug=True
	dash_app.run_server(debug=debug, host='0.0.0.0', port=port)


def init_dashboard(dash_app, raw_data_path, frame_type, channel_map_id):
	
	pil_image = Image.open("assets/image3.png")
	#engine = DataManager("/home/gkokkoro/git/About_time_workarea/sourcecode/data/", "ProtoWIB", 'VDColdbox')
	engine = DataManager(raw_data_path, frame_type, channel_map_id)

	data_files = engine.list_files()
	rich.print(data_files)
	#engine = DataManager("/tmp/", 'VDColdboxChannelMap')
	all_storage = all_data_storage(engine)
	pages, plots, ctrls = ld.get_elements(dash_app = dash_app, engine = engine, storage = all_storage)
	
	layout = []
	layout.append(create_navbar(pages))
	#layout.append(dbc.Container([theme], className="m-4 dbc"))
	layout.append(html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
					    html.A(html.Img(src=pil_image)                          
                            
                        ),
                        html.H1("Just-in-Time"),
						html.H4("(Proto)DUNE: Prompt-Feedback"),
                        html.P(
                            """Select a plot to portray from the navbar above."""
                        ),
						html.Div([ctrl.div for ctrl in ctrls], id = "ctrls_div",style={'fontSize': '12px '}),
                        
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                        dcc.Markdown(
                            """
                            Source: [FiveThirtyEight](https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/master/uber-trip-data)
                            Links: [Source Code](https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-uber-rides-demo) | [Enterprise Demo](https://plotly.com/get-demo/)
                            """
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        
                        html.Div(
                            className="text-padding",
                            children=[
                                
                            ],
                        ),
                        html.Div([plot.div for plot in plots], id = "plots_div",style={'fontSize': '12px '})],
                
                ),
            ],
        )
    ]
))
		
		
		
		
		#html.Div(children=[
       
         #             html.Div(className='row',  # Define the row element
          #                    children=[
           #                      html.Div(className='four columns div-user-controls',children=[html.Div(id="description-card",children=[html.H1("Just-in-Time"), html.H4("(Proto)DUNE: Prompt-Feedback")]),html.Div([ctrl.div for ctrl in ctrls], id = "ctrls_div"),]),
      #Define the left element
            #                      html.Div(className='eight columns div-for-charts bg-grey',children=[html.Div([plot.div for plot in plots], id = "plots_div")])
	  # Define the right element
             #                     ])
              #                  ]))       
	
	
		
		
		
	layout.append(html.Div([dcc.Location(id='url', refresh=False),html.Div(id='page-content')])) 


	#layout.append(dbc.Container([theme], className="m-4 dbc"))
	
	

	#layout.append(load_figure_template(ThemeSwitchAIO))
	init_page_callback(dash_app, all_storage)

	dash_app.layout = html.Div(layout)


def init_page_callback(dash_app, all_storage):
	pages, plots, ctrls = ld.get_elements()
	
	plot_outputs = [Output(plot.id, "style") for plot in plots]
	ctrl_outputs = [Output(ctrl.id, "style") for ctrl in ctrls]


	@dash_app.callback(*ctrl_outputs,*plot_outputs,[Input('url', 'pathname')])

	def page_button_callback(pathname):
		
		pages, plots, ctrls = ld.get_elements()
		style_list = [{"display":"none"} for _ in range(len(plots)+len(ctrls))]
		for page in pages:
			if pathname:
				if f"/{page.id}" in pathname:
					
					return(calculate_page_style_list(page, plots, ctrls, style_list, all_storage))
		return(style_list)


def calculate_page_style_list(page, plots, ctrls, style_list, all_storage):
	needed_plots = []
	needed_ctrls = []
	for plot_n, plot in enumerate(plots):
		if plot.id in page.plots:
			needed_plots.append(plot.id)
			style_list[len(ctrls)+plot_n] = plot.display
			for ctrl in ctrls:
				if (ctrl.id in plot.ctrls) and not (ctrl.id in needed_ctrls):
					needed_ctrls.append(ctrl.id)
	all_storage.update_shown_plots(needed_plots)
	needed_ctrls = get_ctrl_dependancies(ctrls,needed_ctrls)

	for ctrl_n, ctrl in enumerate(ctrls):
		if ctrl.id in needed_ctrls:
			style_list[ctrl_n] = ctrl.display
	return(style_list)

def get_ctrl_dependancies(ctrls,needed_ctrls):
	changed = True
	while changed:
		changed = False
		for ctrl_out in ctrls:
			if ctrl_out.id in needed_ctrls:
				for ctrl_in in ctrls:
					if (ctrl_in.id in ctrl_out.ctrls) and not (ctrl_in.id in needed_ctrls):
						needed_ctrls.append(ctrl_in.id)
						changed = True
	return(needed_ctrls)


if __name__ == "__main__":
	main()
