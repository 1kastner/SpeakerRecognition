# use your python interpreter from your virtual environment

import FeatureExtractor
import InputLoader
import MarkSpeech
import sys


def get_features(sample):
    """
    @param sample:
    @return:
    """
    base_pre_data = InputLoader.get_wave_file(sample)
    preprocessed = MarkSpeech.mark_speaker(base_pre_data)
    return FeatureExtractor.extract_mfcc_60(preprocessed)


def write_features_to_standard_outout(label, features):
    """
    @type label: String
    @param label: The speaker
    @type features: numpy.array
    @param features: The extracted features per window of a single person
    """
    print "@RELATION cogs_speaker"
    for pos, feature in enum(features[0]):
        print "@ATTRIBUTE " + str(pos) + " NUMERIC"
    print "@ATTRIBUTE class {Kamuran,Firat,Marvin}"
    for window in features:
        for feature in window:
            sys.stdout.write(str(feature)+",")
        print label


if __name__ == "__main__":
    # 1st arg: speaker, 2nd arg: wave file name
    write_features_to_standard_outout(sys.argv[1], get_features(sys.argv[2]))
