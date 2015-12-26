# use your python interpreter from your virtual environment

import os
import bob.bio.spear.preprocessor.Base

def get_base_preprocessed_file(file_name):
    """
    @type file_name: String
    @return: (<Hertz>, <numpy array>)
    """
    project_base_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir
    )
    audio_file_path = os.path.join(project_base_dir, "AudioFiles", file_name)
    base_preprocessor = bob.bio.spear.preprocessor.Base()
    return base_preprocessor.read_original_data(audio_file_path)
    #import pkg_resources
    #return base_preprocessor.read_original_data(pkg_resources.resource_filename('bob.bio.spear.test', 'data/sample.wav'))

def extract_mfcc_60(base_preprocessed_data):
    """
    @type base_preprocessed_file:  (<Hertz>, <numpy array>)
    """    
    preprocessor = bob.bio.spear.preprocessor.Energy_2Gauss()
    #@type preprocessed_data: (<Herz>, <numpyArray>, <speaker vs. silence>)
    preprocessed_data = preprocessor(base_preprocessed_data)
    
    extractor = bob.bio.base.load_resource('mfcc-60', 'extractor')
    extracted = extractor(preprocessed_data)
    return extracted
    
if __name__ == "__main__":
    base_pre_data = get_base_preprocessed_file("firat_speakerRecognitionWiki_16khz_mono.wav")
    print extract_mfcc_60(base_pre_data)

    