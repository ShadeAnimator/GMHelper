#!/usr/bin/env python2.7
__author__ = 'nixes'

import sys #used for writing\reading files
from PyQt4 import QtCore, QtGui, uic #PyQt interface
import PyQt4 #just in case
import charOps as co #GMH module containing operations with characters, saving, loading, filling lists.
import dataFiles #GMH module which reads from files and stores game data in itself, also contains arrays of char's stats
import random #RANDOM!!! more random
import numpy as np #pg uses it for something...
import pyqtgraph as pg #pyqt graphs are based on this
import bbc #GMH module with functions to format bbcode, bold, color, etc.
import json #everything is stored as JSON files
import bbcode #pretty printing bbcode into html display window
import actionNodes as nodes #GMH module containing 'nodes', function to be used in Actions
from datetime import datetime #for date and time, obviously


#define color vars
colorStat = dataFiles.PrintColors['stats']
colorName = dataFiles.PrintColors['names']
colorWarn = dataFiles.PrintColors['warn']
colorGood = dataFiles.PrintColors['good']


def roundTr(v):
    # A function which is used in rouding a value from 0 to 1 by a specified in UI threshold.
    tr = graphDialog.missTrSB.value()
    if v > tr:
        v = 1.0
    else:
        v = 0.0
    return v


def showOutput(text):
    #prints output bbcode in one window, and html formatted version in another.
    window.outbox.setText(text)
    window.fancyOutbox.setText(bbcode.render_html(text))
    log("Output written.")

dataFiles.reloadFiles()

def log(text):
    #A function for pretty logging with time and date
    print ">>>",datetime.now(),": "+text
    window.statusbar.showMessage(text,0)

#region CharacterEditFunctions
def addChar():
    #Adds a new character to the list and into the character dict
    name = "New Character"
    dataFiles.Characters.update({name:dataFiles.AllAttrsAndInv})
    window.charList.addItem (name)
    window.char2List.addItem (name)
    log ("Character added: "+name)

def delChar():
    #Deletes selected character from the list and character dict.
    #It uses character's name, not index
    id = window.charList.currentIndex()
    name = window.charList.currentText()

    window.charList.removeItem(id)
    window.char2List.removeItem(id)
    dataFiles.Characters.pop(str(name))
    log ("Character deleted: "+str(name))

def fillCharList():
    #Fills character lists in UI from Characters dict
    for name in dataFiles.Characters:
        window.charList.addItem (name)
        window.char2List.addItem (name)
    log ("Character lists filled")

def fillActionList():
    #Fills actions list from action dict
    for action in dataFiles.Actions:
        window.actionList.addItem (action)
    log ("Action list filled")

def updateChar():
    #Updates character's stats.
    nameBox = CE_Dialog.findChild(QtGui.QLineEdit, "nameBox")
    id = window.charList.currentIndex()
    name = str(window.charList.currentText())
    newkey = str(nameBox.text())

    dataFiles.replaceInDict(dataFiles.Characters, name, newkey)

    #Go through all attributes, using the AllAttributes array, which holds all attributes which should be updated. Matched by name.
    for attr in dataFiles.AllAttributes:
        try:
            spinBox = CE_Dialog.findChild(QtGui.QDoubleSpinBox, "SB_CharAttr_"+attr)
            dataFiles.Characters[str(name)][attr]=spinBox.value()
        except:
            log ("ERROR settings attribute "+str(attr))

    window.charList.insertItem(id,newkey)
    window.charList.removeItem(id+1)
    window.char2List.insertItem(id,newkey)
    window.char2List.removeItem(id+1)

    window.charList.setCurrentIndex(id)
    log ("Character updated.")



#Update attributes of a character editor window
def updateAttrs():
    id = window.charList.currentIndex()
    name = str(window.charList.currentText())

    nameBox = CE_Dialog.findChild(QtGui.QLineEdit, "nameBox")
    nameBox.setText(name)
    for attr in dataFiles.AllAttributes:
        spinBox = CE_Dialog.findChild(QtGui.QDoubleSpinBox, "SB_CharAttr_"+attr)
        try:
            spinBox.setValue(dataFiles.Characters[name][attr])
        except:
            pass

    #INVENTORY
    inventoryDialog.inventoryList.clear()

    for key, value in dataFiles.Characters[name]['inventory'].iteritems():
        try:
            inventoryDialog.inventoryList.addItem(key)
        except:
            print "ERROR: Could not fill the inventory for", key, value
    log ("Attributes shown for character "+name)

def showEditChar():
    CE_Dialog.show()
    log ("Edit character dialog shown")

def saveAllCharacters():
    co.saveAllChars(dataFiles.Characters)
    log ("Characters saved")
#endregion

#region GraphFunctions
def showLuckGraph():
    name = str(window.charList.currentText())
    name2 = str(window.char2List.currentText())
    data1 = []
    data2 = []
    for x in range (0,20):
        char1Roll = 20*round(random.betavariate(dataFiles.Characters[name]['luck'],1),1)
        char2Roll = 20*round(random.betavariate(dataFiles.Characters[name2]['luck'],1),1)
        data1.append(char1Roll)
        data2.append(char2Roll)
    crits1 = []
    crits2 = []
    for i in data1:
        if i == 20:
            crits1.append(i)
    for i in data2:
        if i == 20:
            crits2.append(i)

    output = "CHAR1 CRITS: "+ str(len(crits1))+" FOR "+str(len(data1))+" ROLLS"
    output += "\nCHAR 2CRITS: "+ str(len(crits2))+" FOR "+str(len(data2))+" ROLLS"
    showOutput(output)


    #pw = pg.plot(data, pen='r')   # data can be a list of values or a numpy array
    #pw.plot(data2,pen='b')
    graphDialog.pGraph.clear()
    graphDialog.pGraph.plot(data1, pen='r')
    graphDialog.pGraph.plot(data2, pen='b')
    log ("Luck graph plotted.")

def showDamageGraph():
    Char1 = str(window.charList.currentText())
    Char2 = str(window.char2List.currentText())
    actionData = dataFiles.Actions[str(window.actionList.currentText())]

    data1 = []
    data2 = []
    Ch1 = dataFiles.Characters[Char1].copy()
    Ch2 = dataFiles.Characters[Char2].copy()

    for x in range (0,20):
        mainDice = x
        char1HealthRoll = eval(actionData['Ch2']['Health'])*-1
        char2HealthRoll = eval(actionData['Ch2']['Health'])*-1
        data1.append(char1HealthRoll)
        data2.append(char2HealthRoll)

    graphDialog.pGraph.clear()
    graphDialog.pGraph.plot(data1, pen='r')
    graphDialog.pGraph.plot(data2, pen='b')
    log ("damage graph plotted.")


def showMissGraph():
    rollsNum = graphDialog.rollsNumberSB.value()
    Char1 = str(window.charList.currentText())
    Char2 = str(window.char2List.currentText())
    actionData = dataFiles.Actions[str(window.actionList.currentText())]

    data1 = []
    data2 = []
    Ch1 = dataFiles.Characters[Char1].copy()
    Ch2 = dataFiles.Characters[Char2].copy()

    for x in range (0,rollsNum):
        missDice = roundTr(nodes.roll(1,1,Ch1['dexterity'], Ch2['dexterity']))+3
        missDice2 = roundTr(nodes.roll(1,1,Ch2['dexterity'], Ch1['dexterity']))
        print missDice, missDice2
        data1.append(missDice)
        data2.append(missDice2)

    graphDialog.pGraph.clear()
    graphDialog.pGraph.plot(data1, pen='r')
    graphDialog.pGraph.plot(data2, pen='b')
    log ("Miss graph plotted.")


def showLuckGraphWindow():
    graphDialog.show()
#endregion

def compareStats(before, after): #compare stats before and after and output
    output = ''

    for key, value in after.iteritems():
        try:
            d = value-before[key]
            if key[0].isupper() == False:
                d = d*(-1)
            keyS = key.encode('ascii','ignore')
            valueS = str(value)
            dS=str(d)
            if value != before[key]:
                if d > 0:
                    col = colorGood
                else:
                    col = colorWarn
                output += keyS+": "+valueS+bbc.color("("+dS+")",col)+"; "
            else:
                pass
                #output += key+": "+value+"; "
        except:
            print "Skipped", keyS, valueS, dS
    log ("Stats compared.")
    return output


#Region ACTION FUNCTIONS
def doAction(*args): #main action event handler.
    log ('Action roll!')
    startInventoryUse()
    characterStatus = ''

    actionData = dataFiles.Actions[str(window.actionList.currentText())]
    Char1 = str(window.charList.currentText())
    Char2 = str(window.char2List.currentText())


    #Ch1 and Ch2 store Chars' stats as they were BEFORE action
    Ch1 = dataFiles.Characters[Char1].copy()
    Ch2 = dataFiles.Characters[Char2].copy()

    #VARIABLES FOR ACTIONS
    missDice = roundTr(nodes.roll(1,1,Ch1['dexterity'], Ch2['dexterity']))
    if missDice == 0:
        missed = True
    else:
        missed = False
    mainDice = nodes.roll(1,20,Ch1['luck'],1)
    weaponDamage = 0
    for item, stats in dataFiles.Characters[Char1]['inventory'].iteritems():
        wd = dataFiles.Characters[Char1]['inventory'][item]['Ch1']['Damage']
        if wd > 0:
            weaponDamage += wd
            log ("Adding damage from weapons: "+str(weaponDamage))
    if mainDice == 20:
        crit = dataFiles.configFile['CritMultiplier']
        critText = bbc.color('CRITICAL HIT! Crit mult:'+str(dataFiles.configFile['CritMultiplier']),colorWarn)+'\n\n'
    else:
        crit = 1
        critText = ''

    #Evaluate actions from actionDatabase action

    for attr in dataFiles.AllAttributes:
        if attr == 'Health':
            if dataFiles.Characters[Char1]['Stamina'] > 0:
                influence1 = round(eval(actionData['Ch1'][attr]))
                influence2 = round(eval(actionData['Ch2'][attr]))

                log ("Stamina is above 0, normal damage evaluation: "+str(influence2))
            else:
                log ("Stamina is below  0, divided damage evaluation")
                characterStatus += Char1+ "'s stamina is below 0, damage lowered!"
                influence1 = round(eval(actionData['Ch1'][attr])/10)
                influence2 = round(eval(actionData['Ch2'][attr])/10)
        else:
            log ("Evaluating "+attr+" stat")
            influence1 = round(eval(actionData['Ch1'][attr]))
            influence2 = round(eval(actionData['Ch2'][attr]))

        if (missed and attr != "Stamina"): #If missed skip any influences except for stamina
            log ("Missed, skipping influencing of "+str(attr))
        else:
            log ("Influencing "+str(attr)+": "+str(influence1)+"; "+str(influence2))
            dataFiles.Characters[Char1][attr] += influence1
            dataFiles.Characters[Char2][attr] += influence2

    #damage items in inventory
    inventoryDamage = ''
    if missed == False:
        print "DAMAGING INVENTORY"
        for item, stats in dataFiles.Characters[Char1]['inventory'].iteritems():
            itemD = eval(actionData['Ch1']['itemDamage'])
            if itemD != 0:
                itemD /= round(nodes.roll(1,5,1,1)+1) #Randomise damage to different items. Should be replaced with target system
                dataFiles.Characters[Char1]['inventory'][str(item)]['Durability'] += itemD
                inventoryDamage += Char1+"'s "+item+" durability: "+str(dataFiles.Characters[Char2]['inventory'][str(item)]['Durability'])+"("+str(itemD)+"); \n"
        for item, stats in dataFiles.Characters[Char2]['inventory'].iteritems():
            itemD = eval(actionData['Ch2']['itemDamage'])
            if itemD != 0:
                itemD /= nodes.roll(1,5,1,1)+1 #See above
                dataFiles.Characters[Char2]['inventory'][str(item)]['Durability'] += itemD
                inventoryDamage += Char2+"'s "+item+" durability: "+str(dataFiles.Characters[Char2]['inventory'][str(item)]['Durability'])+"("+str(itemD)+"); \n"

    #print dataFiles.Characters[Char2]

    if missed:
        critText += bbc.color("MISS!\n\n", colorWarn)

    #region Printing output

    if dataFiles.Characters[Char1]['Health'] < -100:
        characterStatus  += bbc.bold(bbc.color(Char1+"'s health dropped below -100! Death suggested!\n", colorWarn))
    elif dataFiles.Characters[Char1]['Health'] < 0:
        characterStatus  += bbc.bold(bbc.color(Char1+"'s health dropped below 0! KO or Death suggested!\n", colorWarn))
    else:
        pass
    if dataFiles.Characters[Char2]['Health'] < -100:
        characterStatus  += bbc.bold(bbc.color(Char2+"'s health dropped below -100! Death suggested!\n", colorWarn))
    elif dataFiles.Characters[Char2]['Health'] < 0:
        characterStatus  += bbc.bold(bbc.color(Char2+"'s health dropped below 0! KO or Death suggested!\n", colorWarn))
    else: pass

    inventoryReport = stopInventoryUse()

    ch1OutputStats = bbc.color(Char1, colorName)+' '+compareStats(Ch1, dataFiles.Characters[Char1])
    ch2OutputStats = bbc.color(Char2, colorName)+' '+compareStats(Ch2, dataFiles.Characters[Char2])
    output = bbc.bold(Char1+" ==> "+Char2+'\n\n'+str(critText)+str(characterStatus)+str(ch1OutputStats)+'\n'+str(ch2OutputStats)+'\n'+str(inventoryDamage)+'\n'+str(inventoryReport)+'\n\n'+bbc.color('Main Dice Roll: ', colorWarn)+str(mainDice))
    showOutput(output)
    #log (json.dumps(dataFiles.Characters, sort_keys=True, indent=4, separators=(',', ': ')))
    log('Action roll done!')
    #endregion

def luckyRoll():
    log ('luck roll!')
    startInventoryUse()
    Char1 = str(window.charList.currentText())
    Char2 = str(window.char2List.currentText())

    luck1 = dataFiles.Characters[Char1]['luck']
    luck2 = dataFiles.Characters[Char2]['luck']

    roll = nodes.roll(1,20,luck1,luck2)

    output = bbc.bold(bbc.color('Luck Roll: ', colorWarn)+str(roll))
    showOutput(output)

    stopInventoryUse()
    log ("Lucky roll done.")


def startInventoryUse():
    log ("Summing up inventory stats and characters'")
    activeChars = {'Ch1':str(window.charList.currentText()),'Ch2':str(window.char2List.currentText())}

    for ch, self in activeChars.iteritems():
        if ch == 'Ch1':
            other = activeChars['Ch2']
        if ch == 'Ch2':
            other = activeChars['Ch1']
        for obj, val in dataFiles.Characters[self]['inventory'].iteritems():
            for stat in dataFiles.AllStats:
                dataFiles.Characters[self][stat] += dataFiles.Characters[self]['inventory'][obj]['Ch1'][stat]
        for obj, val in dataFiles.Characters[other]['inventory'].iteritems():
            for stat in dataFiles.AllStats:
                dataFiles.Characters[self][stat] += dataFiles.Characters[other]['inventory'][obj]['Ch2'][stat]

def stopInventoryUse():
    log ("Reverting characters' stats to normal")
    activeChars = {'Ch1':str(window.charList.currentText()),'Ch2':str(window.char2List.currentText())}
    report = ''
    for ch, self in activeChars.iteritems():
        if ch == 'Ch1':
            other = activeChars['Ch2']
        if ch == 'Ch2':
            other = activeChars['Ch1']
        inventorySelf = dataFiles.Characters[self]['inventory'].copy()
        inventoryOther = dataFiles.Characters[other]['inventory'].copy()
        for obj, val in inventorySelf.iteritems():
            if dataFiles.Characters[self]['inventory'][obj]['Durability'] > 0:
                for stat in dataFiles.AllStats:
                    dataFiles.Characters[self][stat] -= dataFiles.Characters[self]['inventory'][obj]['Ch1'][stat]
            else:
                deleteItem(obj,self)
                report += self+"'s "+str(obj)+" is broken!\n"
        for obj, val in inventoryOther.iteritems():
            if dataFiles.Characters[other]['inventory'][obj]['Durability'] > 0:
                for stat in dataFiles.AllStats:
                    dataFiles.Characters[self][stat] -= dataFiles.Characters[other]['inventory'][obj]['Ch2'][stat]
            else:
                deleteItem(obj,self)
                pass
                #report += other+"'s "+str(obj)+" is broken!\n"

    return report
#endregion


#region INVENTORY FUNCTIONS
def showInventory():
    inventoryDialog.show()

def updateInventoryUIStats():
    name = str(window.charList.currentText())
    try:
        itemName = str(inventoryDialog.inventoryList.currentItem().text())
    except:
        print "Inventory update error. Is it empty?"
    inventoryDialog.durabilityBox.setValue(dataFiles.Characters[name]['inventory'][itemName]['Durability'])
    for x, ch in enumerate(sorted(dataFiles.AllItemAttributes)):
        for i, attr, in enumerate(sorted(dataFiles.AllItemAttributes[ch])):
            spinBox = inventoryDialog.findChild(QtGui.QDoubleSpinBox, "SB_"+ch+"_Attr_"+attr)
            spinBox.setValue(dataFiles.Characters[name]['inventory'][itemName][ch][attr])
    inventoryDialog.nameBox.setText(itemName)
    log ("Inventory UI updated for: "+name+" - "+itemName)


def setItemStats():
    name = str(window.charList.currentText())
    itemName = str(inventoryDialog.inventoryList.currentItem().text())
    newName = str(inventoryDialog.nameBox.text())
    dataFiles.Characters = dataFiles.Characters.copy()


    dataFiles.Characters[name]['inventory'][itemName]['Durability'] = inventoryDialog.durabilityBox.value()
    for x, ch in enumerate(sorted(dataFiles.AllItemAttributes)):
        for i, attr, in enumerate(sorted(dataFiles.AllItemAttributes[ch])):
            spinBox = inventoryDialog.findChild(QtGui.QDoubleSpinBox, "SB_"+ch+"_Attr_"+attr)
            dataFiles.Characters[name]['inventory'][itemName][ch][attr]=spinBox.value()

    if newName != itemName:
        log ("Renaming...")
        dataFiles.replaceInDict(dataFiles.Characters[name]['inventory'], str(itemName), str(newName))
        inventoryDialog.inventoryList.currentItem().setText(newName)
    log ("Item stats set: "+name+" - "+itemName)

def addItem():
    newname, ok = QtGui.QInputDialog.getText(window, 'Input New Item Name', 'Enter new UNIQUE name\nFor now having multiple same objects in the list will break this simple program :( :')

    name = str(window.charList.currentText())

    inventoryDialog.inventoryList.addItem(newname)
    dataFiles.Characters[name]['inventory'].update({str(newname):dataFiles.AllItemAttributesCreation})
    log ("Item added: "+newname+" for "+name)

def deleteItem(itemName,character):
    listWidget = inventoryDialog.inventoryList
    items_list = listWidget.findItems(itemName,QtCore.Qt.MatchExactly)
    for item in items_list:
         r = listWidget.row(item)
         listWidget.takeItem(r)

    dataFiles.Characters[character]['inventory'].pop(itemName, None)
    log ("Item "+itemName+" deleted from "+character)


def deleteSelectedItem():
    log ("Delete selected item")
    selected = str(inventoryDialog.inventoryList.currentItem().text())
    character = str(window.charList.currentText())
    deleteItem(selected, character)
#endregion

def reloadData():
    window.charList.clear()
    window.char2List.clear()
    window.actionList.clear()
    dataFiles.configFile, dataFiles.Characters, dataFiles.Items, dataFiles.Actions, dataFiles.PrintColors = dataFiles.reloadFiles()
    fillCharList()
    fillActionList()
    log ("Data reloaded.")

def printStats():
    #Print characters' stats, all of them for selected chars
    output = ''
    Char1 = str(window.charList.currentText())
    Char2 = str(window.char2List.currentText())

    Ch1 = dataFiles.Characters[Char1]
    Ch2 = dataFiles.Characters[Char2]


    output += bbc.color(Char1+': \n', colorName)
    for key, value in Ch1.iteritems():
        if key != 'inventory':
            output += bbc.color(str(key), colorStat)+": "+str(value)+"; \n"
    output += bbc.color('\n'+Char2+': \n', colorName)
    for key, value in Ch2.iteritems():
        if key != 'inventory':
            output += bbc.color(str(key), colorStat)+": "+str(value)+"; \n"

    output = bbc.bold(output)
    showOutput(output)
    log ("Stats printed")


def loadAnotherGame():
    #Loads another config file.
    fileName = QtGui.QFileDialog.getOpenFileName(window, 'Switch config file (Open another game preset)', dataFiles.config_path, selectedFilter='*.cfg')
    if fileName:
        dataFiles.config_path = fileName
        log ("Config file changed to: "+str(fileName))
        reloadData()

def actionChanged():
    #Update description for action.

    window.statusbar.clearMessage()
    try:
        actionData = dataFiles.Actions[str(window.actionList.currentText())]
        actionDescription = str(actionData["Description"])
        window.statusbar.showMessage(actionDescription,2000)
        window.actionList.setStatusTip(actionDescription)
        log ("Action description updated.")
    except:
        log ("Action description NOT updated. No description or corrupted?")



#========================PYQT UI CODE=============================================

inventoryQTC = "GMH_Inventory.ui"
Ui_Dialog, QtBC = uic.loadUiType(inventoryQTC)

class InventoryWindow (QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.nameBox = QtGui.QLineEdit()
        self.statsLayout.addRow("Name:", self.nameBox)
        self.durabilityBox = QtGui.QDoubleSpinBox()
        self.durabilityBox.setRange(-9999,9999)
        self.statsLayout.addRow("Durability:", self.durabilityBox)
        self.inventoryList.currentItemChanged.connect(updateInventoryUIStats)
        self.setItemPropertiesBtn.clicked.connect(setItemStats)
        self.addItemBtn.clicked.connect(addItem)
        self.removeItemBtn.clicked.connect(deleteSelectedItem)

        for x, ch in enumerate(sorted(dataFiles.AllItemAttributes)):
            self.statsLayout.addRow (ch,QtGui.QLabel('_____'))
            for i, attr in enumerate(sorted(dataFiles.AllItemAttributes[ch])):
                spinBox = QtGui.QDoubleSpinBox()
                self.statsLayout.addRow(attr+":",spinBox)
                spinBox.setRange(-9999,9999)
                spinBox.setObjectName("SB_"+ch+"_Attr_"+attr)



charEditQTC = "GMH_EditCharacter.ui"
Ui_Dialog, QtBC = uic.loadUiType(charEditQTC)

class CharacterEditWindow (QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)

        self.setCharAttrsButton.clicked.connect(updateChar)


        #use setobjectname to set name to use in code
        nameBox = QtGui.QLineEdit()
        self.statsLayout.addRow("Name: ",nameBox)
        nameBox.setObjectName("nameBox")

        for i, attr in enumerate(sorted(dataFiles.AllAttributes)):
            spinBox = QtGui.QDoubleSpinBox()
            self.statsLayout.addRow(attr+":",spinBox)
            spinBox.setRange(-9999,9999)
            spinBox.setObjectName("SB_CharAttr_"+attr)

        self.totalStatsLabel = QtGui.QLabel ('')
        self.statsLayout.addRow("Total stats:", self.totalStatsLabel)

qtGraphQTC = "GMH_TestGraphs.ui" # Enter file here.
Ui_GraphDialog, QtBaseClass = uic.loadUiType(qtGraphQTC)
class GraphWindow (QtGui.QDialog, Ui_GraphDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)

        self.plotLuckBtn.clicked.connect(showLuckGraph)
        self.pGraph = pg.PlotWidget()
        self.verticalLayout.addWidget(self.pGraph)
        self.plotDamageBtn.clicked.connect(showDamageGraph)
        self.missPlotButton.clicked.connect(showMissGraph)

qtCreatorFile = "GHM_MainWindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.__windows = []

        self.setupUi(self)
        self.charList.setInsertPolicy(2)

        #region connections
        self.addCharBtn.clicked.connect(addChar)
        self.delCharBtn.clicked.connect(delChar)

        self.actionDoButton.clicked.connect(doAction)
        self.actionCharacter.triggered.connect(showEditChar)
        self.actionInventory.triggered.connect(showInventory)
        self.actionLoad_Characters_All.triggered.connect(reloadData)
        self.actionSave_Characters_All.triggered.connect(saveAllCharacters)
        self.actionTest_Graph.triggered.connect(showLuckGraphWindow)
        self.actionLoad_Another_Game.triggered.connect(loadAnotherGame)

        self.charList.currentIndexChanged.connect(updateAttrs)
        self.actionList.currentIndexChanged.connect(actionChanged)
        self.luckyDiceButton.clicked.connect(luckyRoll)
        self.printStatsButton.clicked.connect(printStats)
        #self.nameBox.returnPressed.connect(updateChar)
        #end region

        with open(dataFiles.configFile['CSS'],"r") as fh:
            self.setStyleSheet(fh.read())

        def styleDefault():
            with open('flistDefault.css',"r") as fh:
                self.setStyleSheet(fh.read())
        def styleDark():
            with open('flistDark.css',"r") as fh:
                self.setStyleSheet(fh.read())
        def styleBright():
            with open('flistBright.css',"r") as fh:
                self.setStyleSheet(fh.read())

        def openHelpFile():
            import os
            import platform
            opsys = platform.system()

            filename = "Help\\GMHelperHelp.chm"
            if opsys == 'Windows':
                os.system("start "+filename)
            elif opsys == 'Linux':
                os.system("open "+filename)
            else:
                os.system("open "+filename)

        self.actionHelp.triggered.connect(openHelpFile)

        self.actionDefault.triggered.connect(styleDefault)
        self.actionDark.triggered.connect(styleDark)
        self.actionBright.triggered.connect(styleBright)


#Launch and open default window and do basic startup stuff
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    CE_Dialog = CharacterEditWindow(window)
    graphDialog = GraphWindow(window)
    inventoryDialog = InventoryWindow(window)
    window.show()
    #CE_Dialog.show()
    fillCharList()
    fillActionList()

    sys.exit(app.exec_())
