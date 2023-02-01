from .. import page_class

def return_obj():
    text="Raw ADC Waveform for each channel, overlaid with TPs. Time above threshold of the TPs are represented as a white box. Choose the range, as well as the plane and according channel."
    page = page_class.page("Raw Waveforms and TP Display", "13_waveform_vs_tp_page",text)
    page.add_plot("14_waveform_vs_tp_plot")
    return(page)