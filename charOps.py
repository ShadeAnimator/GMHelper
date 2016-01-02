__author__ = 'nixes'

import json
import dataFiles

def fillDefaultCharactersFromList(AllAttributes, AllChars):
    Characters = {}
    for name in AllChars:
        Characters.update({name:AllAttributes})
    return Characters

def saveAllChars(data):
    dataFiles.saveJSON(dataFiles.configFile['Characters'], data)


