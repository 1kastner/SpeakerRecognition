"""
The input loader takes the input from either a wave file or recorded sound and pre-processes it.
That means, all public functions return the tuple (<Hertz>, <numpy array>)
"""

import os
import bob


def get_wave_file(file_name):
    """
    @type file_name: String
    @return: base preprocessed file, format: (<Hertz>, <numpy array>)
    """
    file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            "AudioFiles",
            file_name
    )
    base_preprocessor = bob.bio.spear.preprocessor.Base()
    return base_preprocessor.read_original_data(file_path)

# TODO add microphone resource here
