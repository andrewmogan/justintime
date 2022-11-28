from .. import page_class

def return_obj():
	page = page_class.page("Trigger primitive display", "01_tp_display_page")
	page.add_plot("01_tp_display_plot")
	return(page)