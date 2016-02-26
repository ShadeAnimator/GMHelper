__author__ = 'nixes'

from PyQt4 import QtCore, QtGui, QtWebKit
import os
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver as wd
import time
from prettytable import PrettyTable
import bbcode
import dataFiles
from GMH import ColorsMeta, Colors
import BBCodeEditor_vars as bbvs

class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            def bbc1(code, value, text):
                return "[{0}={1}]{2}[/{0}]".format(code,value,text)

            def bbc(code,text):
                return "[{0}]{1}[/{0}]".format(code,text)

            def makeUrl():
                url, ok = QtGui.QInputDialog.getText(self, self.tr("Get URL"),self.tr("URL:"), QtGui.QLineEdit.Normal)
                cursor = textEdit.textCursor()
                if ok:
                    textEdit.insertPlainText(bbc1("url",str(url),str(cursor.selectedText())))

            def bold():
                cursor = textEdit.textCursor()
                textEdit.insertPlainText(bbc("b",cursor.selectedText()))

            def italic():
                cursor = textEdit.textCursor()
                textEdit.insertPlainText(bbc("i",cursor.selectedText()))

            def underline():
                cursor = textEdit.textCursor()
                textEdit.insertPlainText(bbc("u",cursor.selectedText()))

            def ooc():
                cursor = textEdit.textCursor()
                textEdit.insertPlainText("(("+cursor.selectedText()+"))")

            def collapse():
                cursor = textEdit.textCursor()
                heading, ok = QtGui.QInputDialog.getText(self, self.tr("QInputDialog().getText()"),self.tr("Heading:"), QtGui.QLineEdit.Normal)
                textEdit.insertPlainText(bbc1("collapse",heading,cursor.selectedText()))

            def saveFile():
                file = open(os.path.dirname(os.path.realpath(__file__))+r"\bbc1EditSave.txt", "w")
                saveText = textEdit.toPlainText()
                file.write(saveText)

            def openFile():
                file = open(os.path.dirname(os.path.realpath(__file__))+r"\bbc1EditSave.txt", "r")
                openText = file.read()
                textEdit.setPlainText(openText)

            def color():
                cursor = textEdit.textCursor()
                textEdit.insertPlainText(bbc1("color",str(colorList.currentText()),str(cursor.selectedText())))

            def clipboard():
                textEdit.selectAll()
                textEdit.cut()

            def renderHtlm():
                #region
                header = r'''
                <html>
                    <head>
                        <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
                        <script type="text/javascript">
                            $(function(){
                            $('#example_tree').find('SPAN').click(function(e){
                                $(this).parent().children('UL').toggle();
                            });
                            });
                        </script>

                        <link rel="stylesheet" type="text/css" href="https://static.f-list.net/css/common/default-0.0.10.css?trigger=1446" />
                        <link rel='stylesheet' type='text/css' href='https://static.f-list.net/css/common/character.css?trigger=1446' />
                        <link rel="stylesheet" type="text/css" href="https://static.f-list.net/css/dark.css?trigger=1446" />
                        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
                        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js"></script>
                        <script src='https://static.f-list.net/js/f-list.js?trigger=1446' type='text/javascript'></script>
                        <script src='https://static.f-list.net/js/f-list.utils.js?trigger=1446' type='text/javascript'></script>
                        <script type="text/javascript">
                            $("div.CollapseHeader").toggle(function(){
                            $(this).addClass("ExpandedHeader");
                            }, function () {
                            $(this).removeClass("ExpandedHeader");
                        });

                        $(document).ready(function() {
                        //Slide up and down on click
                        $("div.CollapseHeader").click(function(){
                            $(this).toggleClass('inactive');
                            $(this).parent().next("div.CollapseBlock").slideToggle("slow");
                            });
                        });
                        </script>
                        <link rel="stylesheet" href="https://www.f-list.net/static/images/icons/fa/css/font-awesome.min.css">
                        <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
                        <script src="https://www.google.com/jsapi?key=ABQIAAAA4tvKLKnKwB5W1nL_b_wJXRQMCsOcopUbve-Ru1_bsEbiyzNqWRTAzatggHo_c6fm8l70pM-fvoK3TQ"></script>

                    </head>
                <body>
                <noscript><div id="JSWarning">You need to enable javascript to be able to use this website.</div></noscript>
                <td id="Content" style="min-width: 659px;">
                <div id="tabs" class="ui-tabs ui-widget ui-widget-content ui-corner-all">
                <div id="tabs-1" class="StyledForm ui-tabs-panel ui-widget-content ui-corner-bottom">
                <div class="FormattedBlock" style="word-wrap:break-word;">
                '''
                footer = r'''
                </div>
                </div>
                </div>
                </td>
                    </body>
                </html>
                '''
                #endregion

                content = str(textEdit.toPlainText())
                if cb_cbStatus.isChecked():
                    bbcode.cb_open = True
                else:
                    bbcode.cb_open = False
                #print content
                formattedContent = bbcode.render_html(content)
                html = header+'\n'+formattedContent+'\n'+footer

                textPreview.setHtml(html)
                #textPreview.setUrl(QtCore.QUrl('https://www.f-list.net/c/laura_/'))



            mainQWidget = QtGui.QWidget()
            #region create layouts
            mainLayout = QtGui.QVBoxLayout()
            mainQWidget.setLayout(mainLayout)
            gridLayout1 = QtGui.QGridLayout()
            #endregion
            font = QtGui.QFont()
            font.setPointSize(13)

            boldBtn = QtGui.QPushButton("B")
            boldBtn.clicked.connect(bold)
            boldBtn.setShortcut("Ctrl+B")

            italicBtn = QtGui.QPushButton("I")
            italicBtn.clicked.connect(italic)
            italicBtn.setShortcut("Ctrl+I")

            underlineBtn = QtGui.QPushButton("U")
            underlineBtn.clicked.connect(underline)
            underlineBtn.setShortcut("Ctrl+U")

            urlBtn = QtGui.QPushButton("URL")
            urlBtn.clicked.connect(makeUrl)

            colBtn = QtGui.QPushButton("Collapse")
            colBtn.clicked.connect(collapse)

            oocBtn = QtGui.QPushButton("OOC")
            oocBtn.clicked.connect(ooc)

            saveBtn = QtGui.QPushButton("save")
            saveBtn.clicked.connect(saveFile)
            saveBtn.setShortcut("Ctrl+S")

            loadBtn = QtGui.QPushButton("open")
            loadBtn.clicked.connect(openFile)
            loadBtn.setShortcut("Ctrl+O")

            colorBtn = QtGui.QPushButton("Color")
            colorBtn.clicked.connect(color)
            colorBtn.setShortcut ("Ctrl+P")

            toClipBoardBtn = QtGui.QPushButton("Clipboard")
            toClipBoardBtn.clicked.connect(clipboard)
            toClipBoardBtn.setShortcut ("Ctrl+F")

            colorList = QtGui.QComboBox()
            colorList.addItem("red")
            colorList.addItem("orange")
            colorList.addItem("yellow")
            colorList.addItem("brown")
            colorList.addItem("cyan")
            colorList.addItem("blue")
            colorList.addItem("pink")
            colorList.addItem("purple")


            textEdit = QtGui.QTextEdit()
            textEdit.textChanged.connect(renderHtlm)

            textPreview = QtWebKit.QWebView()
            textPreview.setObjectName('fancyOutbox')
            textPreview.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
            textPreview.settings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
            #QtWebKit.QWebSettings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
            #textPreview.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)

            cb_cbStatus = QtGui.QCheckBox("Collapse Open")
            cb_cbStatus.stateChanged.connect(renderHtlm)


            mainLayout.addLayout(gridLayout1)
            mainLayout.addWidget(textEdit)
            mainLayout.addWidget(textPreview)

            gridLayout1.addWidget(boldBtn,1,1)
            gridLayout1.addWidget(italicBtn,1,2)
            gridLayout1.addWidget(underlineBtn,1,3)
            gridLayout1.addWidget(urlBtn,1,4)
            gridLayout1.addWidget(oocBtn,1,5)
            gridLayout1.addWidget(colBtn,1,6)
            gridLayout1.addWidget(saveBtn,0,1)
            gridLayout1.addWidget(loadBtn,0,2)
            gridLayout1.addWidget(colorList,0,3)
            gridLayout1.addWidget(colorBtn,0,4)
            gridLayout1.addWidget(toClipBoardBtn,0,5)
            gridLayout1.addWidget(cb_cbStatus,0,6)



            self.setCentralWidget(mainQWidget)
            self.resize(600,800)


            self.setWindowTitle("GMH BBCode Editor")

            with open(dataFiles.configFile['CSS'],"r") as fh:
                self.setStyleSheet(fh.read())

            def setStyle(name):
                if name == 'default':
                    css = 'flistDefault.css'
                    name = Colors.scheme_default
                elif name == 'dark':
                    css = 'flistDark.css'
                    pass
                elif name == 'light':
                    css = 'flistBright.css'
                    pass
                else:
                    raise Exception("Bad style name: %s"%name)


            def styleDefault():
                setStyle('default')

            def styleDark():
                setStyle('dark')

            def styleBright():
                setStyle('light')

            styleDark()



if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())