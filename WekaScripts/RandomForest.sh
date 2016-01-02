#!/usr/bin/env bash

# set these to your local environment
PROJECTREPOSITORY="/home/gorgo/Documents/Model/SpeakerRecognition"

RunAlg () {
    FORESTSIZE="-I "${1}
    echo ${FORESTSIZE}
    weka -m3G -c "weka.classifiers.trees.RandomForest -t ${PROJECTREPOSITORY}/results/all.arff -x 2 ${FORESTSIZE}" > "${PROJECTREPOSITORY}/WekaResults/RandomForest-{1}.txt"
}

RunAllRandomForests() {
    for size in 25 50
    do
        RunAlg $size
    done
}

RunAllRandomForests
