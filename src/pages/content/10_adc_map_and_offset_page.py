from .. import page_class

def return_obj():
	page = page_class.page("Trigger Record Display: ADC maps with offset", "10_adc_map_and_offset_page")
	page.add_plot("10_trigger_record_display_plot")
	page.add_plot("11_trigger_record_display_offset_plot")
	return(page)