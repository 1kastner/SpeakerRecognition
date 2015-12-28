# use your python interpreter from your virtual environment

import FeatureExtractor
import InputLoader
import LearningAlgorithm
import Segregator


def run_learning(sample, label):
    base_pre_data = InputLoader.get_wave_file(sample)
    preprocessed = Segregator.mark_speaker(base_pre_data)
    features = FeatureExtractor.extract_mfcc_60(preprocessed)
    LearningAlgorithm.run_training(features, "Firat")


if __name__ == "__main__":
    run_learning("firat_speakerRecognitionWiki_16khz_mono.wav", "Firat")
    LearningAlgorithm.check_sample("firat_speakerRecognitionWiki_16khz_mono.wav", ["Firat"])
