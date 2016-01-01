#!/bin/bash

# set these to your local environment
alias python='/home/marvin/Downloads/bob-2.0.6/bin/python'
HOME=/home/marvin
ARFF_TARGET="$HOME/projectrepository/results"
MAIN=$HOME/projectrepository/code/main.py

# start

python $HOME/projectrepository/code/main.py HEADER > "$ARFF_TARGET/header.tmp"
HEADER="$ARFF_TARGET/header.tmp"

Wiki () {
    python $MAIN $1 $2.wav > $ARFF_TARGET$2"Data.arff"
    cat "$HEADER" "$ARFF_TARGET/$2Data.arff" > "$ARFF_TARGET/$2.arff"
}

Wiki Firat FiratWiki
Wiki Marvin MarvinWiki
Wiki Kamuran KamuranWiki

cat "$HEADER" "$ARFF_TARGET/MarvinWikiData.arff" "$ARFF_TARGET/KamuranWikiData.arff" "$ARFF_TARGET/FiratWikiData.arff" > "$ARFF_TARGET/AllWiki.arff"