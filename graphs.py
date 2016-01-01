__author__ = 'nixes'


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import random

def showGraph(array):
    global curve
    global data
    global ptr
    global p1



    #QtGui.QApplication.setGraphicsSystem('raster')
    app = QtGui.QApplication([])
    #mw = QtGui.QMainWindow()
    #mw.resize(800,800)

    win = pg.GraphicsWindow(title="Graph")
    win.resize(1000,600)
    win.setWindowTitle('Graph')

    # Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias=True)


    p1 = win.addPlot(title="", y=array)
    win.show()



## Start Qt event loop unless running in interactive mode or using pyside.
'''if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()'''