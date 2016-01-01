__author__ = 'nixes'

import random

#This file contains all actions' functions


def roll(dices,sides,b1,b2):
    result = 0
    if b1 <= 0:
        b1 = 1
    if b2 <= 0:
        b2 = 1
    for i in range (0, dices):
        rand = sides*round(random.betavariate(b1,b2),1)
        result += rand
    return result