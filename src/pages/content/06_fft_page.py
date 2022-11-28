from .. import page_class

def return_obj():
	page = page_class.page("FFT", "06_fft_page")
	page.add_plot("06_fft_plot")
	return(page)