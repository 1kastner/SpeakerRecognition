"""
This draws some comparative plots for measurements
"""

import csv
from matplotlib import pyplot


def compare_j48_subtree_raising():
    """
    blue squares: with
    green triangles: without
    """
    pyplot.ylabel('accuracy')
    pyplot.xlabel('confidence')
    with open("J48_comparison.tsv", "r") as o:
        reader = csv.reader(o, delimiter="\t")
        for row in reader:
            break # discard for line
        for row in reader:
            if row[1] == "No":
                g = pyplot.plot(row[0], row[3], "bs", label="With subtree raising")
            else:
                h = pyplot.plot(row[0], row[3], "g^", label="Without subtree raising")
    pyplot.grid(True)
    pyplot.show() 

def compare_confidence_without_subtree_raising():
    pyplot.ylabel('accuracy')
    pyplot.xlabel('confidence')
    with open("J48_comparison.tsv", "r") as o:
        reader = csv.reader(o, delimiter="\t")
        for row in reader:
            break # discard for line
        for row in reader:
            if row[1] == "No":
                pyplot.plot(row[0], row[3], "bs", label="With subtree raising")
    pyplot.grid(True)
    pyplot.show() 

def compare_one_rule():
    pyplot.ylabel('accuracy')
    pyplot.xlabel('bucket size')
    with open("OneRule.tsv", "r") as o:
        reader = csv.reader(o, delimiter="\t")
        for row in reader:
            break # discard for line
        for row in reader:
            print row[0], row[1]
            g = pyplot.plot(float(row[0]), float(row[1]), "bs")
    pyplot.grid(True)
    pyplot.show() 
    
#compare_j48_subtree_raising()
#compare_confidence_without_subtree_raising()
compare_one_rule()
