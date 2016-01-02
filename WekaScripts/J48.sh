#!/usr/bin/env bash

# set these to your local environment
PROJECTREPOSITORY="/home/marvin/projectrepository"

RunAlg () {
    CONFIDENCE="-C "${1}
    OPTS=${2}
    echo run weka -c "weka.classifiers.trees.J48 -t ${PROJECTREPOSITORY}/results/all.arff -x 2 ${OPTS} ${CONFIDENCE}"
    weka -c "weka.classifiers.trees.J48 -t ${PROJECTREPOSITORY}/results/all.arff -x 2 ${OPTS} ${CONFIDENCE}" > "${PROJECTREPOSITORY}/WekaResults/J48${CONFIDENCE}${OPTS}.txt"
}

RunAllJ48() {
    for confidence in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5
    do
        RunAlg $confidence
        RunAlg $confidence -S
    done
}

RunAlg 0.1
