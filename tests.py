__author__ = 'nixes'
#Just a file for testing python commands, math, etc
import dataFiles
import charOps
#defaultConfig = {'Characters':'characterDatabase.txt','Items':'itemDatabase.txt','Actions':'actionDatabase.txt'}
#iniFiles.saveJSON('default.cfg', defaultConfig)

#defaultActions = {'LightAttack':{'Ch1':charOps.AllAttributes,'Ch2':charOps.AllAttributes}}
#iniFiles.saveJSON('actionDatabase.txt', defaultActions)

Ch1 = dataFiles.Characters['Minotaur'].copy()

import actionNodes as nodes
#print nodes.roll(1,20,4,1)
#print eval("nodes.roll(1,20,Ch1['luck'],1)")

