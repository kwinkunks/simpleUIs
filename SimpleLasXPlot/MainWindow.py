'''
Simple las Cross Plot using PyQt4 and pyqtgraph
Copyright 2015 Anthony Torlucci
Distributed under the terms of the GNU General Public License (see gpl.txt for more information)

    This file is part of Simple LAS Cross Plot.

    Simple LAS Cross Plot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Simple LAS Cross Plot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Simple LAS Cross Plot.  If not, see <http://www.gnu.org/licenses/>.
'''

__author__ = 'Anthony Torlucci'
__version__ = '0.0.1'

# TODO: add another checkbox to the DockWidget to fix the axis values for the crossplot
# TODO: add exit png to application just for fun as an example of adding images

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
        # 1 large widget contains the 2 windows divided by a splitter
        self.mwHouseWidget = QWidget()

        # Create 2 Windows: left=logs; right=Xplot
        self.windowLogs = pg.GraphicsWindow()
        self.windowLogs.setBackground('w')
        self.windowXPlot = pg.GraphicsWindow()
        self.windowXPlot.setBackground('w')
        self.splitter = QSplitter()
        #
        self.splitter.addWidget(self.windowLogs)
        self.splitter.addWidget(self.windowXPlot)
        #
        self.winLayout = QHBoxLayout()
        self.winLayout.addWidget(self.splitter)
        self.mwHouseWidget.setLayout(self.winLayout)
        #
        self.setCentralWidget(self.mwHouseWidget)
        #
        #
        self.p1 = self.windowLogs.addPlot(labels={'left' : 'depth'}, title='X axis')
        self.p1.invertY(b=True)
        self.p1.setMouseEnabled(x=False, y=False)
        self.p1.showGrid(x=True, y=True, alpha=0.5)
        # Curve 2: plots on y axis in crossplot
        self.p2 = self.windowLogs.addPlot(labels={'left' : 'depth'}, title='Y axis')
        self.p2.invertY(b=True)
        self.p2.setMouseEnabled(x=False, y=False)
        self.p2.showGrid(x=True, y=True, alpha=0.5)
        #
        # Scatter Plot in column 3 spanning 3 columns
        self.p3 = self.windowXPlot.addPlot(title='CrossPlot')
        self.p3.showGrid(x=True, y=True, alpha=0.5)
        #
        self.createMenuBar()

    def createMenuBar(self):
        # file menu actions:
        importLasAction = QAction('&Import las', self)
        importLasAction.triggered.connect(self.getLogData)
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.triggered.connect(self.close)
        # about menu actions:
        aboutAction = QAction('About ...', self)
        aboutAction.triggered.connect(self.displayAboutMessage)
        # create instance of menuBar
        menubar = self.menuBar()
        # add file menu and file menu actions
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(importLasAction)
        fileMenu.addAction(exitAction)
        #
        aboutMenu = menubar.addMenu('&About')
        aboutMenu.addAction(aboutAction)


    def getLogData(self):
        fname = QFileDialog.getOpenFileName(self, 'Open las File', os.getenv('HOME'), selectedFilter='*.las')
        strfname = str(fname)
        log_file = LASReader(strfname, null_subs=np.nan)
        self.log_df = pd.DataFrame(log_file.data2d, columns = log_file.curves.names, index=log_file.data['DEPTH'])
        # added for crosshairs
        self.startValue = log_file.start
        self.stopValue = log_file.stop
        self.stepValue = log_file.step
        # just to keep things clean
        del log_file
        # add the names of all the curves in the file (now DataFrame) to a list
        self.curvesList = list(self.log_df.columns.values)
        self.createDockWindows()

    def displayAboutMessage(self):
        #
        aboutText = open('about.txt', mode='r').read()
        QMessageBox.about(self, "About Simple UI", aboutText)

    def createDockWindows(self):
        curveSelectionDockWidget = QDockWidget('curve_selection', self)
        curveSelectionDockWidget.setObjectName('CurveSelectionDockWidget')
        curveSelectionDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # create a widget to house checkbox and list widget with QVBoxLayout
        houseWidget = QWidget(self)
        # add checkbox for log scale
        layout = QVBoxLayout()

        logCheckBox1 = QCheckBox('logarithm scale')
        logCheckBox2 = QCheckBox('logarithm scale')

        def setPlotAxes():
            if logCheckBox1.isChecked() and logCheckBox2.isChecked():
                self.p1.setLogMode(x=True, y=False)
                self.p2.setLogMode(x=True, y=False)
                self.p3.setLogMode(x=True, y=True)
            elif logCheckBox1.isChecked() and not logCheckBox2.isChecked():
                self.p1.setLogMode(x=True, y=False)
                self.p2.setLogMode(x=False, y=False)
                self.p3.setLogMode(x=True, y=False)
            elif logCheckBox2.isChecked() and not logCheckBox1.isChecked():
                self.p1.setLogMode(x=False, y=False)
                self.p2.setLogMode(x=True, y=False)
                self.p3.setLogMode(x=False, y=True)
            elif not logCheckBox1.isChecked() and not logCheckBox1.isChecked():
                self.p1.setLogMode(x=False, y=False)
                self.p2.setLogMode(x=False, y=False)
                self.p3.setLogMode(x=False, y=False)
            else:
                print "what other possibilities are there?"

        logCheckBox1.stateChanged.connect(setPlotAxes)
        layout.addWidget(logCheckBox1)
        #
        self.listWidget1 = QListWidget(self) # self?
        for curve in range(len(self.curvesList)):
            item = QListWidgetItem(self.curvesList[curve])
            self.listWidget1.addItem(item)
        self.listWidget1.setCurrentItem(self.listWidget1.item(0)) # sets the p1 to plot the first item in the list
        self.showCurve1()
        self.listWidget1.clicked.connect(self.showCurve1)
        #
        layout.addWidget(self.listWidget1)
        #
        logCheckBox2.stateChanged.connect(setPlotAxes)
        layout.addWidget(logCheckBox2)
        #
        self.listWidget2 = QListWidget(self)
        for curve in range(len(self.curvesList)):
            item = QListWidgetItem(self.curvesList[curve])
            self.listWidget2.addItem(item)
        self.listWidget2.setCurrentItem(self.listWidget2.item(0)) # sets the p2 to plot the first item in the list
        #
        self.showCurve2()
        self.listWidget2.clicked.connect(self.showCurve2)
        #
        layout.addWidget(self.listWidget2)

        houseWidget.setLayout(layout)
        curveSelectionDockWidget.setWidget(houseWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, curveSelectionDockWidget)
        #
        self.showXplot()

    @pyqtSlot()
    def showCurve1(self):
        # Clear plots
        self.p1.clear()
        #
        self.lr1 = pg.LinearRegionItem([self.startValue, self.stopValue], orientation = pg.LinearRegionItem.Horizontal)
        self.lr1.setZValue(-10)
        self.lr1.setBounds([self.startValue, self.stopValue])
        self.p1.addItem(self.lr1)

        def updateLR():
            self.lr2.setRegion(self.lr1.getRegion())
            self.showXplot()

        self.lr1.sigRegionChanged.connect(updateLR)
        #
        depth = np.array(self.log_df['DEPTH'])
        strCurve = str(self.listWidget1.currentItem().text())
        curve = np.array(self.log_df[strCurve])
        self.p1.plot(curve, depth, pen='k')
        #

    @pyqtSlot()
    def showCurve2(self):
        # Clear plots
        self.p2.clear()
        #
        self.lr2 = pg.LinearRegionItem([self.startValue, self.stopValue], orientation = pg.LinearRegionItem.Horizontal)
        self.lr2.setZValue(-10)
        self.lr1.setBounds([self.startValue, self.stopValue])
        self.p2.addItem(self.lr2)

        def updateLR():
            self.lr1.setRegion(self.lr2.getRegion())
            self.showXplot()

        self.lr2.sigRegionChanged.connect(updateLR)
        #
        depth = np.array(self.log_df['DEPTH'])
        strCurve = str(self.listWidget2.currentItem().text())
        curve = np.array(self.log_df[strCurve])
        self.p2.plot(curve, depth, pen='k')

    def showXplot(self):
        self.p3.clear()
        #
        self.p3.setLabel(axis='bottom', text=str(self.listWidget1.currentItem().text()))
        self.p3.setLabel(axis='left', text=str(self.listWidget2.currentItem().text()))
        #
        minReg, maxReg = self.lr1.getRegion()  # returns the depth values associated with the region as a tuple
        # use the DataFrame structure of pandas to quickly get the values associated with these depths
        dataInRegionDF = self.log_df.loc[minReg:maxReg]
        #print dataTEST
        xData = dataInRegionDF[str(self.listWidget1.currentItem().text())]
        yData = dataInRegionDF[str(self.listWidget2.currentItem().text())]
        crossPlot = pg.ScatterPlotItem()
        self.p3.addItem(crossPlot)
        crossPlot.addPoints(x=xData, y=yData)


# =============== END OF SCRIPT =================