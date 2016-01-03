#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GMM.py is basically a VoiceID wrapper (another wrapper for utilizing LIUM speaker 
diarization tools), that generates GMM models for single speaker audio (mono, 16kHz)
files and classifies novel single-speaker audio samples based on these models. It uses
a k-fold cross validation approach via CCR (correct classification rate).

Marvin Kastner
Kamuran Özlem
Fırat Öter
@METU, 2015
"""

import os
import shutil
import sys
import random
import re
from copy import deepcopy
from pydub import AudioSegment
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB



def fetch_samples(speakers):
    """
    @type   speakers: list        
    @param  speakers: a collection of speaker names 
    @return samples: a dictionary of .wav file names per speaker

    This function takes a list of speaker names and fetch corresponding file
    names into a dictionary. 
    """
    
    samples = {}

    for speaker_name in speakers:
    
        dir_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.pardir,
                "AudioFiles",
                "Reformatted",
                "SingleSpeaker",
                speaker_name,
            )    
        
        samples[speaker_name] = []

        for file in os.listdir(dir_path):
            if file.endswith(".wav"):
                audio_file = AudioSegment.from_wav("%s/%s" %(dir_path, file))
                # LIUM uses a 3-second sliding window while gender and bandwith 
                # detection and a 5-second sliding window while segmenting   
                if audio_file.duration_seconds > 5.0:
                    samples[speaker_name].append("%s/%s" %(dir_path, file))

    return samples


def k_fold_sampling(samples, k):
    """
    @type   samples: dictionary        
    @param  samples: a collection of single-speaker .wav files
    @type   k: integer        
    @param  k: an integer value for the k-fold cross validation
    @return k_fold_samples: a dictionary of 'k' sample sets per speaker

    This function takes a dictionary of single-speaker .wav file names in string
    and iterates over them to randomly create 'k' training and test sets per speaker.
    'k' must be smaller or equal to the sample size and greater than zero at all times!
    """

    k_fold_samples = {}

    for speaker_name in samples:

        random.shuffle(samples[speaker_name])
        
        file_list = samples[speaker_name]
        sample_size = len(file_list)
        split_length = sample_size/float(k)
        split_start = 0.0
        k_split = []

        if sample_size < k:
            raise RuntimeError("'k' is larger than the sample size! Pick a smaller 'k' value.")
        elif k == 0:
            raise RuntimeError("'k' should be greater than '0'! Pick a larger 'k' value.")

        while split_start < sample_size:
            k_split.append(file_list[int(split_start):int(split_start+split_length)])
            split_start += split_length

        k_fold_samples[speaker_name] = k_split

    return k_fold_samples


def merge_samples(k_fold_samples, pos):
    """
    @type   k_fold_samples: dictionary        
    @param  k_fold_samples: a dictionary of 'k' sample sets per speaker
    @type   pos: integer        
    @param  pos: an integer value indicating the current fold
    @return merged_samples: a dictionary of two (training and test) sets per speaker

    This function takes a dictionary of 'k' set of samples and chooses the one
    in the current fold position as the training set, while merging the remaining
    ones into the test set.
    """

    merged_samples = {}
    
    for speaker_name in k_fold_samples:
        
        file_list = deepcopy(k_fold_samples[speaker_name])
        training_samples = file_list[pos]
        del file_list[pos]
        test_samples = [file_name for sub_list in file_list for file_name in sub_list]
        merged_samples[speaker_name] = [training_samples, test_samples]

    return merged_samples


def merge_training_samples(merged_samples, pos):
    """
    @type   merged_samples: dictionary        
    @param  merged_samples: a collection of training and test samples
    @type   pos: integer        
    @param  pos: an integer value indicating the current fold
    @return merged_training_samples: a collection of training and test samples

    This function takes all the files in the training set and merge them into a 
    single .wav file.
    """

    merged_training_samples = deepcopy(merged_samples)

    for speaker_name in merged_samples:
        for i, file in enumerate(merged_samples[speaker_name][0]):
            
            if i == 0:
                training_file = AudioSegment.from_wav(file)
            else:
                training_file += AudioSegment.from_wav(file)
        
        training_file_name = "Training%s%s.wav" %(speaker_name, pos) 
        training_file.export(training_file_name, format="wav")
        merged_training_samples[speaker_name][0] = training_file_name

    return merged_training_samples


def build_gmm_model(merged_training_samples, pos):
    """
    @type   merged_training_samples: dictionary        
    @param  merged_training_samples: a collection of training and test samples
    @type   pos: integer        
    @param  pos: an integer value indicating the current fold
    @return database: a database of GMM model files per speaker

    This function takes a dictionary of single-speaker .wav file names in string
    and iterates over them to create a database of speaker specific GMM-models.
    """

    database = GMMVoiceDB("ModelDatabaseFold%s" %(pos))

    for speaker_name in merged_training_samples:
        database.add_model(merged_training_samples[speaker_name][0][:-4], speaker_name)

    return database


def k_fold_cross_validation(k_fold_samples, k):
    """
    @type   k_fold_samples: dictionary        
    @param  k_fold_samples: a dictionary of 'k' sample sets per speaker
    @type   k: integer        
    @param  k: an integer value for the k-fold cross validation
    @return overall_accuracy_ratings: a dictionary of accuracies per fold and per speaker

    This function takes a dictionary of 'k' set of samples per speaker, merges the samples
    into two (training and test) sets per fold, merges the files in the training set into a 
    single .wav file per fold, generates a database of GMM models by training the single 
    merged training file per fold, tests the files in the test set on the database per fold
    and calculates the accuracy of each test case.  
    """


    def _get_duration_from_segment(string):
        """
        @type   string: string
        @param  string: a single line from the output of the print_segments() function 
                        of VoiceID
        @return a tuple of four integers corresponding to the hour, minute, second and 
        millisecond of the segment length

        This function takes the print_segments() output and parses it into its scales of
        time in integer format.
        """
        match = re.match(r"(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d),(?P<millisecond>\d\d\d)", string)
        return (
            int(match.group("hour")), 
            int(match.group("minute")), 
            int(match.group("second")), 
            int(match.group("millisecond"))
        )


    overall_accuracy_ratings = []

    for pos in range(k):
        
        merged_samples = merge_samples(k_fold_samples, pos)
        merged_training_samples = merge_training_samples(merged_samples, pos)   
        database = build_gmm_model(merged_training_samples, pos)

        speaker_accuracy_ratings = {}
        test_overall_size = 0

        for speaker_name in merged_training_samples:
            
            test_files = merged_training_samples[speaker_name][1]
            # test_speaker_sample_size = len(test_files) 
            # test_overall_sample_size += test_speaker_size
            correct_classifications_size = 0
            
            for file in test_files:
                
                test = Voiceid(database, file) 

                """ 
                supress the print function within Voiceid.extract_speakers()
                !!! Find a different strategy; standart python interpreter does not
                allow write access to sys.stdout.write !!!

                Ex:
                import os, sys
                f = open(os.devnull, 'w')
                sys.stdout = f
                """
                write = sys.stdout.write
                sys.stdout.write = lambda x: x
                test.extract_speakers()
                sys.stdout.write = write

                for _cluster in test.get_clusters():
                    
                    cluster = test.get_cluster(_cluster)
                    class_name = re.search("\((.*)\)", str(cluster)).group(1)
                    
                    """ 
                    redirect the print function within Voiceid.print_segments()
                    !!! Find a different strategy; standart python interpreter does not
                    allow write access to sys.stdout.write !!!
                    """
                    segments = []
                    sys.stdout.write = lambda x: segments.append(x)
                    cluster.print_segments()
                    sys.stdout.write = write

                    for segment in segments:

                        if not segment.strip(): 
                            continue
                        
                        start, stop = segment.split(" to ")
                        
                        hour, minute, second, millisecond = _get_duration_from_segment(start)
                        start = hour*3.6e6 + minute*6e4 + second*1e3 + millisecond
                        
                        hour, minute, second, millisecond = _get_duration_from_segment(stop)
                        stop = hour*3.6e6 + minute*6e4 + second*1e3 + millisecond
                        
                        segment_size = stop - start
                        test_overall_size += segment_size

                        if class_name == speaker_name:
                            correct_classifications_size += segment_size

            speaker_accuracy_ratings[speaker_name] = {"Correct Classification" : correct_classifications_size, "Fold" : pos}
        
        overall_accuracy_ratings.append([speaker_accuracy_ratings, {"Test Sample Size" : test_overall_size, "Fold" : pos}])

    return overall_accuracy_ratings


def print_results(overall_accuracy_ratings, speakers, k):
    """
    @type   overall_accuracy_ratings: list
    @param  overall_accuracy_ratings: a list of statistical information per speaker per fold
    @type   speakers: list        
    @param  speakers: a collection of speaker names 
    @type   k: integer        
    @param  k: an integer value for the k-fold cross validation
    
    This function prints the accuracy ratings beautifully into a file. Accuracy is evaluated
    based on a simple accuracy measure, CRR (Correct Recognition Rate), which is the ratio of 
    correctly classified instances to the overall sample size.
    """

    results_dir_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.pardir,
                "VoiceidResults",
            )

    results_file = open("%s/GMM_Results.txt" %(results_dir_path), "w")
    results_file.write(">>> %s-Fold Cross-Validation via Correct Recognition Rate (CRR) <<<\n\n\n" %(k))

    fold_accuracies = []

    for fold in overall_accuracy_ratings:
         
        fold_speaker_ratings = deepcopy(fold[0])
        fold_test_sample_size = fold[1]["Test Sample Size"] 
        fold_number = fold[1]["Fold"] 

        results_file.write("**********\nFold No: %s\n**********\n\n" %(fold_number))
        results_file.write("Test Sample Size: %s ms (in milliseconds)\n\n" %(fold_test_sample_size))

        fold_correct_classification = 0

        for speaker_name in speakers:

            speaker_correct_classification = fold_speaker_ratings[speaker_name]["Correct Classification"]
            results_file.write("Speaker Name: %s --> Correct Classification: %s ms\n" %(speaker_name, speaker_correct_classification))
            fold_correct_classification += speaker_correct_classification

        fold_accuracy = round(100*fold_correct_classification/fold_test_sample_size, 2)
        fold_accuracies.append(fold_accuracy)
        results_file.write("\nFold Accuracy: %s%%\n\n" %(fold_accuracy))

    model_accuracy = round(sum(fold_accuracies)/k, 2)

    results_file.write("\n>>> The %s-fold accuracy of this model is: %s%% <<<" %(k, model_accuracy))

    results_file.close()


"""
Check clean_trash() function for errors!
"""
def clean_trash(speakers):
    """ 
    @type   speakers: list
    @param  speakers: a list of speaker names in string
    
    This function removes all unnecessary files generated during execution from_wav
    both data and script directiories. It only allows to keep GMM models generated
    for speakers per fold and the accuracy results.
    """

    for speaker_name in speakers:

        data_dir_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.pardir,
                "AudioFiles",
                "Reformatted",
                "SingleSpeaker",
                speaker_name,
            )

        for file in os.listdir(data_dir_path):
            if (
                not file.endswith(".wav") 
                and not file.startswith(".") 
                and os.path.isfile("%s%s" %(data_dir_path, file))
            ):
                os.remove("%s%s" %(data_dir_path, file))

            elif os.path.isdir("%s%s" %(data_dir_path, file)):
                shutil.rmtree("%s%s" %(data_dir_path, file))

    script_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    for file in os.listdir(script_dir_path):
        if (
            not file.endswith(".py") 
            and not file.startswith(".")
            and os.path.isfile("%s%s" %(script_dir_path, file))
        ):
            os.remove("%s%s" %(script_dir_path, file))
                  

if __name__ == "__main__":

    speakers = ["Marvin", "Kamuran", "Firat"]
    k = 2

    samples = fetch_samples(speakers)
    k_fold_samples = k_fold_sampling(samples, k)
    overall_accuracy_ratings = k_fold_cross_validation(k_fold_samples, k)
    print_results(overall_accuracy_ratings, speakers, k)
    clean_trash(speakers)