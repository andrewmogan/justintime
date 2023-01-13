from .. import page_class

def return_obj():
	text="Scatter plot of FW trigger primitives in each offline channel. The histograms count how many trigger primitives there are to understand the presence of a hot spot. They display the level of activity per channel."
	page = page_class.page("Trigger primitive display", "01_tp_display_page",text)
	page.add_plot("01_tp_display_plot")
	return(page)