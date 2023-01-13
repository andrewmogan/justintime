from .. import page_class

def return_obj():
	text="FFT Phase."
	page = page_class.page("FFT_Phase", "07_fft_phase_page",text)
	page.add_plot("07_fft_phase_plot")
	return(page)