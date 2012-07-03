import multiprocessing
from scipy import signal
import itertools
import numpy

def _get_correlation(args):
    samples1, samples2 = args
    corr = signal.correlate(samples1, samples2, mode="same")
    return corr

def _get_fft_correlation(samples1, samples2):
    samples2 = samples2[::-1]
    corr = signal.fftconvolve(samples1, samples2)
    return corr

def correlate(samples1, samples2, method="corr"):
    """
    This code currently produces wrong results, will be useful after multithreaded aspects are fixed
    """
    samples1 = samples1.astype(float)
    samples2 = samples2.astype(float)
    samples_list = numpy.array_split(samples1, multiprocessing.cpu_count() - 1)
    worker_pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() -1)

    if method=="corr":
        results = worker_pool.map(_get_correlation, itertools.izip(samples_list, itertools.repeat(samples2)))
    elif method=="fft":
        results = worker_pool.map(_get_fft_correlation, itertools.izip(samples_list, itertools.repeat(samples2)))
    else:
        return None

    correlation = numpy.concatenate(results).astype(samples1.dtype)
    return correlation

def get_offset(samples1, samples2, samplerate):
    # Calculate correlation between samples

    correlation = _get_fft_correlation(samples1, samples2)
    # Find maximum positive value
    max = numpy.argmax(correlation)
    # Now calculate actual offset in seconds
    # 0 offset will have a peak at len(samples2)
    offset = float(len(samples2) - max) / float(samplerate)
    return offset