from .. import page_class

def return_obj():
	page = page_class.page("Mean and STD", "05_mean_std_page")
	page.add_plot("04_mean_plot")
	page.add_plot("05_std_plot")
	return(page)