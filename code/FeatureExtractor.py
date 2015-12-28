"""
The feature extractor gathers the different feature extractors used for the project including their configuration.
"""

import numpy
import bob.bio.spear.extractor.Cepstral


def extract_mfcc_60(preprocessed_data):
    """
    @param preprocessed_data: (<Hertz>, <numpyArray>, <0:below, 1:above threshold>) as it is produced by the segregator
    @return: numpy.array

    takes the processed data which assumably belongs to one person and tries to identify this person.
    """
    extractor = bob.bio.spear.extractor.Cepstral(
            win_length_ms=20,
            win_shift_ms=10,
            n_filters=24,
            dct_norm=False,
            f_min=0.0,
            f_max=4000,
            delta_win=2,
            mel_scale=True, # if this is false, it is lfcc
            with_energy=True,
            with_delta=True,
            with_delta_delta=True,
            n_ceps=19,  # 0-->18
            pre_emphasis_coef=0.95,
            features_mask=numpy.arange(0, 60),
            normalize_flag=True,
    )
    return extractor(preprocessed_data)
