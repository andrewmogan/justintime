from .. import page_class

def return_obj():
	text="Fast Fourier Transform Phase for planes Z,V,U. Choose the run data file and according trigger record to portray."
	page = page_class.page("FFT Phase", "07_fft_phase_page",text)
	page.add_plot("07_fft_phase_plot")
	return(page)