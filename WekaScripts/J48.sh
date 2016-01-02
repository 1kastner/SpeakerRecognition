#!/usr/bin/env bash

# set these to your local environment
PROJECTREPOSITORY="E:/uni/metu/CogsML/projectrepository"
WEKADIR="C:/Program Files (x86)/Weka-3-6"

# desired weka settings
WEKASETTINGS="-classpath \"${WEKADIR}/weka.jar\""

RunAlg () {
    CONFIDENCE="-C"${1}
    OPTS=${2}
    echo "Run weka: weka.classifiers.trees.J48 -t ${PROJECTREPOSITORY}/results/all.arff -x 2 ${OPTS} ${CONFIDENCE}"
    #java "${WEKASETTINGS} weka.classifiers.trees.J48 -t ${PROJECTREPOSITORY}/results/all.arff -x2 ${OPTS} ${CONFIDENCE} > ${PROJECTREPOSITORY}/WekaResults/J48${CONFIDENCE}${OPTS}.txt"
    java "${WEKASETTINGS} weka.classifiers.trees.J48"
    # -t ${PROJECTREPOSITORY}/results/all.arff -x2 ${OPTS} ${CONFIDENCE} > ${PROJECTREPOSITORY}/WekaResults/J48${CONFIDENCE}${OPTS}.txt
}

for confidence in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5
do
    echo "I am not working"
    # RunAlg $confidence
    # RunAlg $confidence -S
done
