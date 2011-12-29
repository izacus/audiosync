from scipy import signal
import scipy.io.wavfile
import numpy as np

from filter_plot import mfreqz
from spectrogram.audio_demo import spectrogram, display_spectrogram

def remove_channel(samples):
    return samples[:, 0]

def band_pass_filter(samples, samplerate, low_hz, high_hz):
    taps = 201
    cutoff_low = float(low_hz)
    cutoff_high = float(high_hz)
    nyquist = samplerate / 2.0

    fir_window = signal.firwin(taps,
                               cutoff=[cutoff_low / nyquist, cutoff_high / nyquist],
                               pass_zero=False,
                               window="blackman")
    filtered_samples = scipy.signal.lfilter(fir_window,1,samples)
    filtered_samples = filtered_samples.astype(samples.dtype)

    return filtered_samples

if __name__ == "__main__":
    (samplerate, samples) = scipy.io.wavfile.read("file-c.wav")
    if samples[0].size > 1:
        samples = remove_channel(samples)

    filtered_audio = band_pass_filter(samples, samplerate, 400, 3000)
    scipy.io.wavfile.write("filtered.wav", samplerate, filtered_audio)