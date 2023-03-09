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
from dash_bootstrap_templates import load_figure_template


@click.command()
@click.option('-p', '--port', type=int, default=8001)
@click.argument('raw_data_path', type=click.Path(exists=True, file_okay=False))
@click.argument('channel_map_id', type=click.Choice(['VDColdbox', 'ProtoDUNESP1', 'PD2HD', 'VST']))
@click.argument('frame_type', type=click.Choice(['ProtoWIB', 'WIB']))
@click.argument("template",type=click.Choice(['light','dark']),default='light')


def main(raw_data_path :str, port: int, channel_map_id:str, frame_type: str,template:str):

	channel_map_id += 'ChannelMap'
	theme=([dbc.themes.FLATLY if template=='light' else dbc.themes.DARKLY])
	rich.print("Light mode" if theme==[dbc.themes.FLATLY] else "Dark mode")
	dash_app = Dash(__name__,external_stylesheets=theme)

	init_dashboard(dash_app, raw_data_path, frame_type, channel_map_id,template)
	debug=True
	dash_app.run_server(debug=debug, host='0.0.0.0', port=port)


def init_dashboard(dash_app, raw_data_path, frame_type, channel_map_id,template):
	pil_image = Image.open("assets/image3.png")
	#engine = DataManager("/home/gkokkoro/git/About_time_workarea/sourcecode/data/", "ProtoWIB", 'VDColdbox')
	engine = DataManager(raw_data_path, frame_type, channel_map_id)

	data_files = engine.list_files()
	rich.print(data_files)
	#engine = DataManager("/tmp/", 'VDColdboxChannelMap')
	all_storage = all_data_storage(engine)
	pages, plots, ctrls = ld.get_elements(dash_app = dash_app, engine = engine, storage = all_storage,theme=template)
	
	layout = []
	layout.append(create_navbar(pages))

	layout.append(html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
					    html.A(html.Img(src=pil_image),style={"marginLeft":"0.8em"}),
                        html.H2("(Proto)DUNE Prompt-Feedback: Just-in-Time",style={"fontSize":"12px","marginBottom":"2em"}),
					
						html.H2("   "),
						html.H2(id="text_page"),
						# html.P( id = "pages_div",style={'fontSize': '12px '}),
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
                       
                    ],
                ),
	
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts",
                    children=[
                        
                        html.Div(
                            className="text-padding",
                            children=[
                                
                            ],
                        ),
                        html.Div([plot.div for plot in plots], id = "plots_div",style={'fontSize': '14px '})],
                
                ),
			
	])]
))    		
	
	layout.append(html.Div([dcc.Location(id='url', refresh=False),html.Div(id='page-content')])) 
	
	init_page_callback(dash_app, all_storage)

	dash_app.layout = html.Div(layout)


def init_page_callback(dash_app, all_storage):
	pages, plots, ctrls = ld.get_elements()
	
	page_output=[Output("text_page","children")]
	plot_outputs = [Output(plot.id, "style") for plot in plots]
	ctrl_outputs = [Output(ctrl.id, "style") for ctrl in ctrls]

	@dash_app.callback(page_output,[Input('url', 'pathname')])

	def show_page(pathname):
		pages, plots, ctrls = ld.get_elements()
		for page in pages:
			
			if pathname:
				
				if f"/{page.id}" in pathname:
					
					return([page.name])
			if pathname=='/':
				return(["Select a plot from the menu above"])

				
	@dash_app.callback(*ctrl_outputs,*plot_outputs,[Input('url', 'pathname')])
	
	def page_button_callback(pathname):

		pages, plots, ctrls = ld.get_elements()
		style_list = [{"display":"none"} for _ in range(len(plots)+len(ctrls))]

		for page in pages:
			
			if pathname:
				
				if f"/{page.id}" in pathname:
					page_output=page.name
					return(calculate_page_style_list(page, plots, ctrls, style_list, all_storage))
					
		return(style_list)	

	@dash_app.callback(Output("02_description_ctrl", "is_open"),Input("open", "n_clicks"), Input("close", "n_clicks"),[State("02_description_ctrl", "is_open")],)
	
	def toggle_modal(n1, n2, is_open):

		if n1 or n2:
			return not is_open
		return is_open

	@dash_app.callback([Output("plot_description","children")],[Input('url', 'pathname')])
	
	def show_description(pathname):
		pages, plots, ctrls = ld.get_elements()
		for page in pages:
			
			if pathname:
				
				if f"/{page.id}" in pathname:
					
					return([page.text])
			if pathname=='/':
				return(["Just-in-Time is a prompt feedback tool designed for ProtoDune. It assesses recorded data coming from detector and trigger, with plots that extract complicated information to examine data quality and fragility. Particularly, trigger record displays are provided that allow users to choose run files and trigger records to analyze and compare. A variety of plots is included, which can be found on the navigation bar. "])

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