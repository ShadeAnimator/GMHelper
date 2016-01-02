__author__ = 'nixes'
import json
import os
import sys

config_name = 'default.cfg'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, config_name)


def loadJSON(fileName):
    file = open (fileName, 'r')
    data = json.load(file)
    return data

def saveJSON(fileName, data):
    file = open (fileName, 'w')
    json.dump(data,file, indent=True)

def reloadFiles():
    #Reload data files. Load button and startup.
    configFile = loadJSON(config_path)
    Characters = loadJSON(configFile['Characters'])
    Items = loadJSON(configFile['Items'])
    Actions = loadJSON(configFile['Actions'])
    PrintColors = loadJSON(configFile['PrintColors'])
    print "Data files loaded"
    return configFile, Characters, Items, Actions, PrintColors

AllAttributes = {"Health":100, "Stamina":100, "Arousal":0, "Consciousness":100, "strength":8,"endurance":8,"dexterity":8,"luck":8}
InvItems = {"Axe":{"durability":10,"self":AllAttributes, "other":AllAttributes}, "Armor":{"durability":10,"self":AllAttributes, "other":AllAttributes}}
AllAttrsAndInv = {"Health":100, "Stamina":100, "Arousal":0, "Consciousness":100, "strength":8,"endurance":8,"dexterity":8,"luck":8, "inventory":{}}

AllItemAttributesBase = {'Damage':0,"strength":0,"endurance":0,"dexterity":0,"luck":0}
AllItemAttributes = {'Ch1':AllItemAttributesBase,'Ch2':AllItemAttributesBase}
AllItemAttributesCreation = {'Ch1':AllItemAttributesBase,'Ch2':AllItemAttributesBase, 'Durability':0}

AllStats = ["strength","endurance","dexterity","luck"]

def replaceInDict(dic, oldkey, newkey):
    if newkey!=oldkey:
      dic[newkey] = dic.pop(oldkey)
    print "Replaced",str(oldkey),"with",str(newkey)

configFile, Characters, Items, Actions, PrintColors = reloadFiles()