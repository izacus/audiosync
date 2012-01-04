import scipy
from scipy import signal
import numpy
from filtering import band_pass_filter, downsample
from matplotlib import pyplot

if __name__ == "__main__":
    print "Loading and processing file1..."
    (samplerate, audio1) = scipy.io.wavfile.read("file-c.wav")
    audio1 = band_pass_filter(audio1, samplerate, 400, 3000)
    audio1,samplerate = downsample(audio1, samplerate, 3000)

    print "Loading and processing file2..."
    (samplerate, audio1) = scipy.io.wavfile.read("file-c2.wav")
    audio2 = band_pass_filter(audio1, samplerate, 400, 3000)
    audio2,samplerate = downsample(audio1, samplerate, 3000)

    print "Calculating correlation..."
    corr = signal.correlate(audio1[0:600000], audio2[800000:815000], mode="same")
    print corr
    print "Maximum",  corr.max()
    print "Avg: ", numpy.mean(corr)
    print "Dev: ", numpy.std(corr)

    graph_file = open("plot.gnu", "w")
    counter = 0
    for number in corr:
        graph_file.write("%s %s\n" % (counter, number))
        counter += 1
    graph_file.close()



