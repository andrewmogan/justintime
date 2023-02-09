from .. import page_class

def return_obj():
	text="FFT per Channel"
	page = page_class.page("FFT per Channel", "14_fft_per_channel_page",text)
	page.add_plot("15_fft_per_channel_plot")
	return(page)