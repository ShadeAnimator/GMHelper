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
first_save_load = True


def loadJSON(fileName):
    print "Loading JSON: '%s'" % fileName
    if not os.path.exists(fileName):
        fileName = os.path.basename(fileName).split('_', 1)[-1]
        fileName = os.path.join(application_path, fileName)
        print "File not found, trying default version: '%s'" % fileName
    file = open (fileName, 'r')
    data = json.load(file)
    print "JSON loaded"
    return data

def saveJSON(fileName, data):
    print "Saving JSON", fileName
    file = open (fileName, 'w')
    json.dump(data,file, indent=True)
    print "JSON saved"

def reloadFiles():
    #Reload data files. Load button and startup.
    configFile = loadJSON(config_path)
    config_dir = os.path.dirname(str(config_path))
    Characters = loadJSON(os.path.join(config_dir, configFile['Characters']))
    Items = loadJSON(os.path.join(config_dir, configFile['Items']))
    Actions = loadJSON(os.path.join(config_dir, configFile['Actions']))
    PrintColors = loadJSON(os.path.join(config_dir, configFile['PrintColors']))
    print "Data files loaded"
    return configFile, Characters, Items, Actions, PrintColors

AllAttributes = {"Health":100, "Stamina":100, "Arousal":0, "Consciousness":100, "strength":8,"endurance":8,"dexterity":8,"luck":8}
InvItems = {"Axe":{"durability":10,"self":AllAttributes, "other":AllAttributes}, "Armor":{"durability":10,"self":AllAttributes, "other":AllAttributes}}
AllAttrsAndInv = {"Health":100, "Stamina":100, "Arousal":0, "Consciousness":100, "strength":8,"endurance":8,"dexterity":8,"luck":8, "inventory":{}}

AllItemAttributesBase = {'Damage':0,"strength":0,"endurance":0,"dexterity":0,"luck":0}
AllItemAttributes = {'Ch1':AllItemAttributesBase,'Ch2':AllItemAttributesBase}
AllItemAttributesCreation = {'Ch1':AllItemAttributesBase,'Ch2':AllItemAttributesBase, 'Durability':0}

AllStats = ["strength","endurance","dexterity","luck"]

cappedStats = ['Health', 'Stamina']

def replaceInDict(dic, oldkey, newkey):
    if newkey!=oldkey:
      dic[newkey] = dic.pop(oldkey)
    print "Replaced",str(oldkey),"with",str(newkey)

configFile, Characters, Items, Actions, PrintColors = reloadFiles()
