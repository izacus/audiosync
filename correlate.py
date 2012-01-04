import multiprocessing
import scipy
from scipy import signal
import itertools
import numpy
from filtering import band_pass_filter, downsample

CORRELATION_WIDTH = 20000

def _get_correlation(args):
    samples1, samples2 = args
    corr = signal.correlate(samples1, samples2, mode="same")
    return corr

def correlate(samples1, samples2):
    samples1 = samples1.astype(float)
    samples2 = samples2.astype(float)
    samples_list = numpy.array_split(samples1, multiprocessing.cpu_count())
    worker_pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = worker_pool.map(_get_correlation, itertools.izip(samples_list, itertools.repeat(samples2)))
    correlation = numpy.concatenate(results).astype(samples1.dtype)
    return correlation

if __name__ == "__main__":
    print "Loading and processing file1..."
    (samplerate, audio1) = scipy.io.wavfile.read("ping.wav")
    audio1 = band_pass_filter(audio1, samplerate, 400, 3000)
    audio1,samplerate = downsample(audio1, samplerate, 3000)

    print "Loading and processing file2..."
    (samplerate, audio1) = scipy.io.wavfile.read("ping2.wav")
    audio2 = band_pass_filter(audio1, samplerate, 400, 3000)
    audio2,samplerate = downsample(audio1, samplerate, 3000)

    scipy.io.wavfile.write("f1.wav", samplerate, audio1)
    scipy.io.wavfile.write("f2.wav", samplerate, audio2)

    print "Calculating correlation..."
    a1_center = len(audio1) / 2
    a2_center = len(audio2) / 2
    samples1 = audio1
    samples2 = audio2[a2_center - (CORRELATION_WIDTH / 2):a2_center + (CORRELATION_WIDTH / 2)]
    corr = correlate(samples1, samples2)

    max = numpy.argmax(corr)
    print "Audio2 center is at %s shift %s " % (a2_center, (max - a1_center))
    print "Maximum",  corr.max()
    print "Avg: ", numpy.mean(corr)
    print "Dev: ", numpy.std(corr)
    print "Max index: %s(%s)" % (max, max / float(samplerate))

    graph_file = open("plot.gnu", "w")
    counter = 0
    for number in corr:
        graph_file.write("%s %s\n" % (counter, number))
        counter += 1
    graph_file.close()



