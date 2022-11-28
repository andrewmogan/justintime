from .. import page_class

def return_obj():
	page = page_class.page("Trigger Record Display: ADC maps", "08_adc_map_page")
	page.add_plot("10_trigger_record_display_plot")
	return(page)