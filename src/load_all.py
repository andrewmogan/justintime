import os
import importlib

pages = []
plots = []
ctrls = []
run_new = True

def loader(path, *args, ignore = []):
	objects = []
	file_list = os.listdir(f"{os.path.dirname(__file__)}/{path}/content")
	for file in file_list:
		if file not in ignore and (file[-3:] == ".py"):
			module = importlib.import_module(f"{path}.content.{file[:-3]}")
			objects.append(module.return_obj(*args))
	objects.sort(key=lambda obj: obj.id)
	return(objects)

def get_elements(dash_app = [], engine = [], storage = [],theme=[]):
	global pages, plots, ctrls, run_new
	if run_new:
		pages = loader("pages")
		plots = loader("plots", dash_app, engine, storage,theme)
		ctrls = loader("controls", dash_app, engine)
		run_new = False
	return(pages, plots, ctrls)








