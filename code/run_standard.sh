#!/bin/bash
alias python='/home/marvin/Downloads/bob-2.0.6/bin/python'
HOME=/home/marvin
ARFF_TARGET="$HOME/projectrepository/results"
python $HOME/projectrepository/code/main.py HEADER > "$ARFF_TARGET/header.tmp"
HEADER="$ARFF_TARGET/header.tmp"
MAIN=$HOME/projectrepository/code/main.py

Wiki () {
    python $MAIN $1 $2.wav > $2"Data.arff"
    cat $HEADER "$ARFF_TARGET"/"$2Data.arff" > "$ARFF_TARGET"/"$2Wiki.arff"
}

Wiki Firat FiratWiki
Wiki Marvin MarvinWiki
Wiki Kamuran KamuranWiki

cat HEADER "$ARFF_TARGET/MarvinWikiData.arff" "$ARFF_TARGET/KamuranWikiData.arff" "$ARFF_TARGET/FiratWikiData.arff" > "$ARFF_TARGET/AllWiki.arff"
