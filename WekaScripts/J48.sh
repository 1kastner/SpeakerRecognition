#!/usr/bin/env bash

# set these to your local environment
PROJECTREPOSITORY="/home/marvin/projectrepository"

RunAlg () {
    CONFIDENCE="-C "${1}
    OPTS=""
    weka -m2G -c "weka.classifiers.trees.J48 -t ${PROJECTREPOSITORY}/results/all.arff -x 2 ${OPTS} ${CONFIDENCE}" > "${PROJECTREPOSITORY}/WekaResults/J48-C${1}${2}.txt"
}

RunAllJ48() {
    RunAlg 0.2
    RunAlg 0.3

    #for confidence in 0.35 0.4 0.45 0.5
    #do
    #    RunAlg $confidence
    #    RunAlg $confidence S
    #done

}

RunAllJ48
