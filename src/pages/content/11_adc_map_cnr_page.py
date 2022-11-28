from .. import page_class

def return_obj():
	page = page_class.page("Trigger Record Display: ADC maps CNR", "11_adc_map_cnr_page")
	page.add_plot("12_cnr_plot")
	return(page)