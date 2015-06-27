'''
Simple las Curve Viewer using PyQt4 and pyqtgraph
Copyright 2015 Anthony Torlucci
Distributed under the terms of the GNU General Public License (see gpl.txt for more information)

    This file is part of Simple LAS Curve Viewer.

    Simple LAS Curve Viewer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Simple LAS Curve Viewer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Simple LAS Curve Viewer.  If not, see <http://www.gnu.org/licenses/>.
'''

__author__ = 'Anthony Torlucci'
__version__ = '0.0.2'

# import python standard modules
import os

# import 3rd party libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import pandas as pd
import numpy as np

# import local python
from las import LASReader

class Window(QMainWindow):
    log_df = pd.DataFrame()
    curvesList = []

    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('Simple las Curve Viewer')
        self.window = pg.GraphicsWindow()
        self.setCentralWidget(self.window)
        self.window.setBackground('w')
        self.p1 = self.window.addPlot(labels={'left' : 'depth'}, title='Region Selection')
        self.p1.invertY(b=True)
        self.p1.setMouseEnabled(x=False, y=False)
        self.p1.showGrid(x=True, y=True, alpha=0.5)
        self.p2 = self.window.addPlot(title = 'Zoom on Selected Region')
        self.p2.invertY(b=True)
        self.p2.setMouseEnabled(x=False, y=False)
        self.p2.showGrid(x=True, y=True, alpha=0.5)
        #
        self.createMenuBar()

    def createMenuBar(self):
        # file menu actions:
        importLasAction = QAction('&Import las', self)
        importLasAction.triggered.connect(self.getLogData)
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.triggered.connect(self.close)
        # create instance of menuBar
        menubar = self.menuBar()
        # add file menu and file menu actions
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(importLasAction)
        fileMenu.addAction(exitAction)

    def getLogData(self):
        fname = QFileDialog.getOpenFileName(self, 'Open las File', os.getenv('HOME'), selectedFilter='*.las')
        strfname = str(fname)
        log_file = LASReader(strfname, null_subs=np.nan)
        self.log_df = pd.DataFrame(log_file.data2d, columns = log_file.curves.names, index=log_file.data['DEPTH'])
        # just to keep things clean
        del log_file
        # add the names of all the curves in the file (now DataFrame) to a list
        self.curvesList = list(self.log_df.columns.values)
        self.createDockWindows()

    def createDockWindows(self):
        curveSelectionDockWidget = QDockWidget('curve_selection', self)
        curveSelectionDockWidget.setObjectName('CurveSelectionDockWidget')
        curveSelectionDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # create a widget to house checkbox and list widget with QVBoxLayout
        houseWidget = QWidget(self) # self?
        # add checkbox for log scale
        layout = QVBoxLayout()
        logCheckBox = QCheckBox('logarithm scale')
        def changeAxisScale():
            if logCheckBox.isChecked():
                self.p1.setLogMode(x=True, y=False)
                self.p2.setLogMode(x=True, y=False)
            else:
                self.p1.setLogMode(x=False, y=False)
                self.p2.setLogMode(x=False, y=False)
        logCheckBox.stateChanged.connect(changeAxisScale)
        layout.addWidget(logCheckBox)
        #
        self.listWidget = QListWidget(self) # self?
        for curve in range(len(self.curvesList)):
            item = QListWidgetItem(self.curvesList[curve])
            self.listWidget.addItem(item)
        self.listWidget.doubleClicked.connect(self.showCurve)
        #
        layout.addWidget(self.listWidget)
        houseWidget.setLayout(layout)
        curveSelectionDockWidget.setWidget(houseWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, curveSelectionDockWidget)

    @pyqtSlot()
    def showCurve(self):
        # Clear plots
        self.p1.clear()
        self.p2.clear()
        #
        lr = pg.LinearRegionItem([1000, 6000], orientation = pg.LinearRegionItem.Horizontal)
        lr.setZValue(-10)
        self.p1.addItem(lr)
        def updatePlot():
            self.p2.setYRange(*lr.getRegion(), padding=0)
        def updateRegion():
            lr.setRegion(self.p2.getViewBox().viewRange()[0])
        lr.sigRegionChanged.connect(updatePlot)
        #self.p2.sigXRegionChanged.connect(updateRegion) # x and y should be locked so this is not needed.
        updatePlot()
        #
        depth = np.array(self.log_df['DEPTH'])
        strCurve = str(self.listWidget.currentItem().text())
        curve = np.array(self.log_df[strCurve])
        self.p1.plot(curve, depth, pen='k')
        self.p2.plot(curve, depth, pen='k')

# =============== END OF SCRIPT =================
