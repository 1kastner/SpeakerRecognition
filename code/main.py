# use your python interpreter from your virtual environment

import FeatureExtractor
import InputLoader
import LearningAlgorithm
import Segregator


def get_features(sample):
    """
    @param sample:
    @return:
    """
    base_pre_data = InputLoader.get_wave_file(sample)
    preprocessed = Segregator.mark_speaker(base_pre_data)
    return FeatureExtractor.extract_mfcc_60(preprocessed)


def run_learning(sample, label):
    features = get_features(sample)
    LearningAlgorithm.run_training(features, "Firat")


if __name__ == "__main__":
    for window in get_features("firat_speakerRecognitionWiki_16khz_mono.wav"): # a 20ms window
        import sys
        for pos, feature in enumerate(window): #value of vector
            sys.stdout.write(str(feature))
            if len(window) - 1 != pos:
                sys.stdout.write(",")
        print ";"

