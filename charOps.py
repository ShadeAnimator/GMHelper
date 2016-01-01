__author__ = 'nixes'

import json
import dataFiles



def fillDefaultCharactersFromList(AllAttributes, AllChars):
    Characters = {}
    for name in AllChars:
        Characters.update({name:AllAttributes})
    return Characters




#AllChars = ["Laura","Minotaur"]
#testDict = fillDefaultCharactersFromList(AllAttrsAndInv,  AllChars)
#saveJSON("characterDatabase.txt", testDict)
#testDict = loadJSON("characterDatabase.txt")
#print testDict

def saveAllChars(data):
    dataFiles.saveJSON(dataFiles.configFile['Characters'], data)


