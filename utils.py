import numpy

def get_audio_from_file(filename):
    """
    Extracts audio data from video file in mono
    Returns tuple of (sample_rate, numpy samples array)
    """
    import pyvideo

    source = pyvideo.load(filename, skip_video=True)
    video_ts = source.get_next_video_timestamp()

    num_samples = source.duration * source.audio_format.sample_rate * source.audio_format.channels
    if source.audio_format.sample_size == 16:
        file_data = numpy.zeros((num_samples,), dtype=numpy.int16)
    else:
        assert source.audio_format.sample_size == 8
        file_data = numpy.zeros((num_samples,), dtype=numpy.int8)

    counter = 0
    last = 0
    while True:
        audio_data = source.get_audio_data()

        if audio_data is None:
            break

        # Consume video frames which prevents memory leakage
        while video_ts < audio_data.timestamp:
            source.get_next_video_frame()
            video_ts = source.get_next_video_timestamp()
            if video_ts is None:
                break

            percent = int(video_ts * 100 / source.duration)
            if percent != last:
                last = percent

        data = numpy.fromstring(audio_data.get_string_data(), dtype=file_data.dtype)
        if counter + data.shape[0] < file_data.shape[0]:
            file_data[counter:counter + data.shape[0]] = data
            counter += len(data)
        else:
            break

    # Reshape to match channels
    assert source.audio_format.channels == 2 or source.audio_format.channels == 1
    if source.audio_format.channels == 2:
        if len(file_data) % 2 == 1: file_data = numpy.resize(file_data, len(file_data) + 1)    # Pad with zero if length is odd
        file_data = numpy.reshape(file_data, (-1, source.audio_format.channels))
        # Flatten channels to mono if audio is stereo
        file_data = (file_data[:,0] + file_data[:, 1]) / 2
    return file_data, source.audio_format.sample_rate