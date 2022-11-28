from .. import page_class

def return_obj():
	page = page_class.page("FFT_Phase", "07_fft_phase_page")
	page.add_plot("07_fft_phase_plot")
	return(page)