from .. import page_class

def return_obj():
    text="Fast Fourier Transform for planes Z,V,U. Choose the run data file and according trigger record to portray."
    page = page_class.page("FFT", "06_fft_page",text)
    page.add_plot("06_fft_plot")
    return(page)