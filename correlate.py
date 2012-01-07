import multiprocessing
import scipy
from scipy import signal
import itertools
import numpy
import time
from filtering import band_pass_filter, downsample

CORRELATION_WIDTH = 20000

def _get_correlation(args):
    samples1, samples2 = args
    corr = signal.correlate(samples1, samples2, mode="same")
    return corr

def _get_fft_correlation(args):
    samples1, samples2 = args
    corr = signal.fftconvolve(samples1, samples2[::-1])
    return corr

def correlate(samples1, samples2, method="corr"):
    samples1 = samples1.astype(float)
    samples2 = samples2.astype(float)
    samples_list = numpy.array_split(samples1, multiprocessing.cpu_count() - 1)
    worker_pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() -1)

    if method=="corr":
        results = worker_pool.map(_get_correlation, itertools.izip(samples_list, itertools.repeat(samples2)))
    elif method=="fft":
        results = worker_pool.map(_get_fft_correlation, itertools.izip(samples_list, itertools.repeat(samples2)))
    else:
        results = None

    correlation = numpy.concatenate(results).astype(samples1.dtype)
    return correlation

if __name__ == "__main__":
    print "Loading and processing file1..."
    (samplerate, audio1) = scipy.io.wavfile.read("file.wav")
    audio1 = band_pass_filter(audio1, samplerate, 400, 3000)
    audio1,samplerate = downsample(audio1, samplerate, 3000)

    print "Loading and processing file2..."
    (samplerate, audio2) = scipy.io.wavfile.read("file2.wav")
    audio2 = band_pass_filter(audio2, samplerate, 400, 3000)
    audio2,samplerate = downsample(audio2, samplerate, 3000)

    print "Calculating correlation..."
    start = time.time()
    corr = correlate(audio1, audio2, method="fft")
    end = time.time()

    corr = numpy.clip(corr, 0, corr.max)

    # Filter correlation with median filter
    max = numpy.argmax(corr)
    print "Samplerate: %s" % (samplerate,)
    print "Max index: %s (shift %s)" % (max, (len(audio2) - max) / float(samplerate))
    print "Took %s s." % ((end - start,))

    graph_file = open("plot.gnu", "w")
    counter = 0
    for number in corr:
        graph_file.write("%s %s\n" % (counter, number))
        counter += 1
    graph_file.close()



