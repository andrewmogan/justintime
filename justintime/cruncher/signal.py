from scipy import signal
import pandas as pd

# Signal filtering
def butter_highpass(cutoff, fs, order=7):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return pd.DataFrame(y, columns=data.columns)


# Calculate The FFT of CE trigger fragment
def calc_fft(df: pd.DataFrame):
    df_fft = df.apply(np.fft.fft)
    df_fft2 = np.abs(df_fft) ** 2
    freq = np.fft.fftfreq(8192, 0.5e-6)
    df_fft['Freq'] = freq
    df_fft2['Freq'] = freq
    # Cleanup fft2 for plotting
    df_fft2 = df_fft2[df_fft2['Freq']>0]
    df_fft2 = df_fft2.set_index('Freq')
    return df_fft, df_fft2