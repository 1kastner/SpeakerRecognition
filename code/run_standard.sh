#!/bin/bash

# set these to your local environment
alias python='/home/marvin/Downloads/bob-2.0.6/bin/python'
HOME=/home/marvin
ARFF_TARGET="$HOME/projectrepository/results"
SINGLE_SPEAKER="$HOME/projectrepository/AudioFiles/SingleSpeaker"
MAIN=$HOME/projectrepository/code/main.py

# start

python $HOME/projectrepository/code/main.py HEADER > "$ARFF_TARGET/header.tmp"
HEADER="$ARFF_TARGET/header.tmp"

Wiki () {
    python $MAIN $1 $2.wav > "$ARFF_TARGET/$2Data.arff"
    cat "$HEADER" "$ARFF_TARGET/$2Data.arff" > "$ARFF_TARGET/$2.arff"
}

# Wiki Firat FiratWiki
# Wiki Marvin MarvinWiki
# Wiki Kamuran KamuranWiki
# cat "$HEADER" "$ARFF_TARGET/MarvinWikiData.arff" "$ARFF_TARGET/KamuranWikiData.arff" "$ARFF_TARGET/FiratWikiData.arff" > "$ARFF_TARGET/AllWiki.arff"

SingleSpeaker () {
    echo "Reset $1SingleSpeakerData.arff"
    cat /dev/null > ${ARFF_TARGET}"/"${1}"SingleSpeakerData.arff"
    for file in $SINGLE_SPEAKER/$1/*
    do
        echo "process "$file
        echo "save in "${ARFF_TARGET}"/"${1}"SingleSpeakerData.arff"
        python $MAIN $1 $file >> ${ARFF_TARGET}"/"${1}"SingleSpeakerData.arff"
    done
    cat ${ARFF_TARGET}"/"${1}"SingleSpeakerData.arff" >> ${ARFF_TARGET}"/all.arff"
}

cat "$HEADER" > ${ARFF_TARGET}"/all.arff"
SingleSpeaker Kamuran
SingleSpeaker Firat
SingleSpeaker Marvin

#cat ${ARFF_TARGET}"/KamuranSingleSpeakerData.arff" ${ARFF_TARGET}"/FiratSingleSpeakerData.arff" ${ARFF_TARGET}"/MarvinSingleSpeakerData.arff" >> ${ARFF_TARGET}"/all.arff"
