"""
The segmenter takes a longer input file and cuts it whenever the energy threshold falls below a certain value.
Further it indicates during which parts of the file the speaker speaks.
"""
import bob.bio.spear.preprocessor


def _load_algorithm():
    """
    @return: bob.bio.base.preprocessor
    """
    return bob.bio.spear.preprocessor.Energy_2Gauss(
        max_iterations=10,
        convergence_threshold=0.0005,
        variance_threshold=0.0005,
        win_length_ms=20.,
        win_shift_ms=10.,
        smoothing_window=10
    )


def mark_speaker(base_preprocessed_data):
    """
    @param base_preprocessed_data: (<Hertz>, <numpy array>) as it is produced by the InputLoader
    @return: (<Hertz>, <numpyArray>, <0:below, 1:above threshold>)

    This method only allows a single speaker in the data
    """

    # so far the preprocessor only gets the standard arguments. These can be played with.
    preprocessor = _load_algorithm()
    return preprocessor(base_preprocessed_data)
