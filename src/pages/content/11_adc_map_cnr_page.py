from .. import page_class

def return_obj():
	text="ADC Map CNR."
	page = page_class.page("Trigger Record Display: ADC maps CNR", "11_adc_map_cnr_page",text)
	page.add_plot("12_cnr_plot")
	return(page)