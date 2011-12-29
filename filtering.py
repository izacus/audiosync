import multiprocessing
from scipy import signal
import scipy.io.wavfile
import itertools
import numpy

def remove_channel(samples):
    return samples[:, 0]

def _do_filter(args):
    samples, fir_window = args
    filtered_samples = scipy.signal.lfilter(fir_window,1,samples)
    return filtered_samples

def band_pass_filter(samples, samplerate, low_hz, high_hz):
    taps = 61
    cutoff_low = float(low_hz)
    cutoff_high = float(high_hz)
    nyquist = samplerate / 2.0

    fir_window = signal.firwin(taps,
                               cutoff=[cutoff_low / nyquist, cutoff_high / nyquist],
                               pass_zero=False,
                               window="blackman")

    # Split samples in no. of processor subarrays
    samples_list = numpy.array_split(samples, multiprocessing.cpu_count())
    worker_pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = worker_pool.map(_do_filter, itertools.izip(samples_list, itertools.repeat(fir_window)))
    filtered_samples = numpy.concatenate(results).astype(samples.dtype)
    print "Results: ", filtered_samples
    return filtered_samples

def downsample(samples, samplerate, max_frequency):
    # First find minimum samplerate multiplier to satisfy nyquist
    q = 1
    while samplerate / (q + 1) > (max_frequency * 2):
        q += 1

    print "Found decimation factor: ", q
    decimated_samples = signal.decimate(samples, q).astype(samples.dtype)
    return decimated_samples, samplerate / q

if __name__ == "__main__":
    (samplerate, samples) = scipy.io.wavfile.read("liberatio.wav")
    if samples[0].size > 1:
        samples = remove_channel(samples)

    filtered_audio = band_pass_filter(samples, samplerate, 400, 3000)
    filtered_audio,samplerate = downsample(filtered_audio, samplerate, 3000)
    scipy.io.wavfile.write("filtered.wav", samplerate, filtered_audio)

