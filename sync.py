import logging
from audiosync import utils, filtering, correlate

logger = logging.getLogger(__name__)

def preprocess_audio(audio, samplerate):
    """
    Preprocesses audio track for matching
    """
    audio = filtering.band_pass_filter(audio, samplerate, 400, 3000)
    audio, new_samplerate = filtering.downsample(audio, samplerate, 3000)
    audio = filtering.normalize_volume(audio)
    return audio, new_samplerate

WINDOW_SIZE = 60    # Search window size in seconds

def find_offset(target, source, source_offset):
    """
    Finds piece of source file around source_offset in target file
    target - File in which to match the piece (file path or (numpy array, samplerate) tuple of preprocessed samples)
    source - File to extract piece of file from (file path or (numpy array, samplerate) tuple of preprocessed samples)
    source_offset - offset of piece of interest in source file (in seconds)

    Returns offset in target file in seconds
    """
    if isinstance(target, basestring):
        logger.debug("Target file passed as filepath, loading...")
        target_audio, target_samplerate = utils.get_audio_from_file(target)
        target_audio, target_samplerate = preprocess_audio(target_audio, target_samplerate)
        logger.debug("Loaded.")
    else:
        target_audio, target_samplerate = target

    if isinstance(source, basestring):
        logger.debug("Source file passed as filepath, loading...")
        source_audio, source_samplerate = utils.get_audio_from_file(source)
        source_audio, source_samplerate = preprocess_audio(source_audio, source_samplerate)
        logger.debug("Done.")
    else:
        source_audio, source_samplerate = source

    assert target_samplerate == source_samplerate

    # Take 20 second stretch of audio to look for correlation
    start_index = max(0, (source_offset * source_samplerate) - ((WINDOW_SIZE * source_samplerate) / 2))
    end_index = min(len(source_audio) - 1, (source_offset * source_samplerate) + ((WINDOW_SIZE * source_samplerate)/ 2))

    source_slice = source_audio[start_index:end_index]
    offset, correlation = correlate.get_offset(source_slice, target_audio, source_samplerate)
    return offset
