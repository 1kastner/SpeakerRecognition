#!/bin/bash
alias python='/home/marvin/Downloads/bob-2.0.6/bin/python'
HOME=/home/marvin
python $HOME/projectrepository/code/main.py Firat FiratWiki.wav > "$HOME/projectrepository/results/FiratWiki.arff"
python $HOME/projectrepository/code/main.py Marvin MarvinWiki.wav > "$HOME/projectrepository/results/MarvinWiki.arff"
python $HOME/projectrepository/code/main.py Kamuran KamuranWiki.wav > "$HOME/projectrepository/results/KamuranWiki.arff"
cat $HOME/projectrepository/results/FiratWiki.arff $HOME/projectrepository/results/MarvinWiki.arff $HOME/projectrepository/results/KamuranWiki.arff > "$HOME/projectrepository/results/AllWiki.arff"
