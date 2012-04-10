from audiosync import utils, filtering

def preprocess_audio(audio, samplerate):
    """
    Preprocesses audio track for matching
    """
    audio = filtering.band_pass_filter(audio, samplerate, 400, 3000)
    audio, new_samplerate = filtering.downsample(audio, samplerate, 3000)
    return audio, new_samplerate


def find_offset(target, source, source_offset):
    """
    Finds piece of source file around source_offset in target file
    target - File in which to match the piece (file path or (numpy array, samplerate) tuple of preprocessed samples)
    source - File to extract piece of file from (file path or (numpy array, samplerate) tuple of preprocessed samples)
    source_offset - offset of piece of interest in source file (in seconds)

    Returns offset in target file in seconds
    """

    if isinstance(target, basestring):
        target_audio, target_samplerate = utils.get_audio_from_file(target)
        target_audio, target_samplerate = preprocess_audio(target_audio, target_samplerate)
    else:
        target_audio, target_samplerate = target

    if isinstance(source, basestring):
        source_audio, source_samplerate = utils.get_audio_from_file(source)
        source_audio, source_samplerate = preprocess_audio(source_audio, source_samplerate)
    else:
        source_audio, source_samplerate = source

    assert target_samplerate == source_samplerate