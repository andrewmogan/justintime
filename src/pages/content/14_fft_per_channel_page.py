from .. import page_class

def return_obj():
	text="Fast Fourier Transform per Channel. Choose the range, the plane and the according channel number. "
	page = page_class.page("FFT per Channel", "14_fft_per_channel_page",text)
	page.add_plot("15_fft_per_channel_plot")
	return(page)