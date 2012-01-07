#!/bin/env python
# -*- coding: utf-8 -*-
import scipy

import sys
from correlate import get_offset
from filtering import band_pass_filter, downsample

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: main file1.wav file2.wav"

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    # Load and do band-pass filtering on the input files
    print "Loading and pre-processing %s..." % (filename1,)
    (samplerate, audio1) = scipy.io.wavfile.read(filename1)
    audio1 = band_pass_filter(audio1, samplerate, 400, 3000)    # Human voice usually spans 400-3000Hz
    audio1,samplerate1 = downsample(audio1, samplerate, 3000)
    print "Loading and pre-processing %s..." % (filename2,)
    (samplerate, audio2) = scipy.io.wavfile.read(filename2)
    audio2 = band_pass_filter(audio2, samplerate, 400, 3000)
    audio2,samplerate2 = downsample(audio2, samplerate, 3000)

    if samplerate1 != samplerate2:
        print "ERROR: Audio re-sampling isn't implemented yet. Make sure both input files are sampled at same rate."
    samplerate = samplerate1

    offset,correlation = get_offset(audio1, audio2, samplerate)
    print "Offset is %s s." % (offset,)