__author__ = 'nixes'

import charOps as co
import PySide
import pysideuic
import random
import pyqtgraph.examples

def roll(dices,sides):
    result = 0
    for x in range(0,dices) :
        x = random.betavariate(10, 100)
        result += x
    return result




import graphs

ax = []
for x in range (0,15):
    y = 20*round(random.betavariate(6,1),1)
    ax.append(y)
crits = []
for i in ax:
    print i
    if i == 20:
        crits.append(i)
print "CRITS:", len(crits), "FOR", len(ax), "ROLLS"

graphs.showGraph(ax)