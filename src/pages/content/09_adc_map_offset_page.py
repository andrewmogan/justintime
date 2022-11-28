from .. import page_class

def return_obj():
	page = page_class.page("Trigger Record Display: ADC maps only offset", "09_adc_map_offset_page")
	page.add_plot("11_trigger_record_display_offset_plot")
	return(page)