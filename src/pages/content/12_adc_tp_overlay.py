from .. import page_class

def return_obj():
	text="Map of ADC values with FW Trigger Primitives overlayed in each offline channel. If only the ADC Plot is desired, simply tap the TP Trace button on the plot and the TPs will not be overlayed. There are a number of controls to choose from, including which plane to portray and the amplitude range. Moreover, the user can opt for an interactive plot or static image and remove the offset. The x-axis is shifted and the initial time stamp is shown in the plot."
	page = page_class.page("Trigger Record Display: ADC maps and TPs", "12_adc_tp_overlay_page",text)
	page.add_plot("13_adc_tp_plot")
	return(page)