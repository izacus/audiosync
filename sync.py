from audiosync import utils

def find_offset(target, source, source_offset):
    """
    Finds piece of source file around source_offset in target file
    target - File in which to match the piece (file path or numpy array of preprocessed samples)
    source - File to extract piece of file from (file path or numpy array of preprocessed samples)
    source_offset - offset of piece of interest in source file (in seconds)

    Returns offset in target file in seconds
    """

    if isinstance(target, basestring):
        target_audio = utils.get_audio_from_file(target)
    else:
        target_audio = target

    if isinstance(source, basestring):
        source_audio = utils.get_audio_from_file(source)
    else:
        source_audio = source


