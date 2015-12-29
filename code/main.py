# use your python interpreter from your virtual environment

import FeatureExtractor
import InputLoader
import LearningAlgorithm
import Segregator
import sys


def get_features(sample):
    """
    @param sample:
    @return:
    """
    base_pre_data = InputLoader.get_wave_file(sample)
    preprocessed = Segregator.mark_speaker(base_pre_data)
    return FeatureExtractor.extract_mfcc_60(preprocessed)


def write_features_to_stdout(features):
    """
    @type features: numpy.array
    @param features: The extracted features per window of a single person
    """
    for window in features:
        for pos, feature in enumerate(window):  # value of vector
            sys.stdout.write(str(feature))
            if len(window) - 1 != pos:
                sys.stdout.write(",")
        print ";"


def run_learning(sample, label):
    features = get_features(sample)
    LearningAlgorithm.run_training(features, "Firat")


if __name__ == "__main__":
    write_features_to_stdout(get_features(sys.argv[1]))
