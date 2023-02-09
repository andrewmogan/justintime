from .. import page_class

def return_obj():
	text="Mean and Standard Deviation of ADC Values in each plane. Choose the run data file and according trigger record to portray."
	page = page_class.page("Mean and STD", "05_mean_std_page",text)
	page.add_plot("04_mean_plot")
	page.add_plot("05_std_plot")
	return(page)