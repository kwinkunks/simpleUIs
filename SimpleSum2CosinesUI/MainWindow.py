'''
Simple Sum 2 Cosines UI using PyQt4 and pyqtgraph
Copyright 2015 Anthony Torlucci
Distributed under the terms of the GNU General Public License (see gpl.txt for more information)

    This file is part of Simple LAS Curve Viewer.

    Simple Sum 2 Cosines UI is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Simple Sum 2 Cosines UI is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Simple Sum 2 Cosines UI.  If not, see <http://www.gnu.org/licenses/>.
'''

__author__ = 'Anthony Torlucci'
__version__ = '0.0.1'

# import python standard modules

# import 3rd party libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import numpy as np

# import local python

class Window(QMainWindow):

    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('Simple Sum 2 Cosines UI')
        self.window = pg.GraphicsWindow()
        self.setCentralWidget(self.window)
        self.window.setBackground('w')
        self.p1 = self.window.addPlot(labels={'left' : 'amplitude'}, title='f(t) = cos(2*pi*f*t + phi)')
        self.p1.setMouseEnabled(x=False, y=False)
        self.p1.showGrid(x=True, y=True, alpha=0.5)
        self.p1.setYRange(-1, 1)
        self.window.nextRow()
        self.p2 = self.window.addPlot(labels={'left' : 'amplitude'}, title='g(t) = cos(2*pi*f*t + phi)')
        self.p2.setMouseEnabled(x=False, y=False)
        self.p2.showGrid(x=True, y=True, alpha=0.5)
        self.p2.setYRange(-1, 1)
        self.window.nextRow()
        self.pSum = self.window.addPlot(labels={'left' : 'amplitude'}, title='h(t) = f(t) + g(t)')
        self.pSum.setMouseEnabled(x=False, y=False)
        self.pSum.showGrid(x=True, y=True, alpha=0.5)
        self.pSum.setYRange(-2, 2)
        #
        self.phi1 = 0.0 # initialize the phase value for the top plot: f(t)
        self.freq1 = 0.0 # initialize frequency value for the top plot: f(t)
        self.phi2 = 0.0 # initialize the phase value for the middle plot: g(t)
        self.freq2 = 0.0 # initialize frequency for the middle plot: g(t)
        self.t = np.linspace(0.0, 1.0, num=1000, endpoint=True)
        self.fillIt = False
        #
        self.phi1Label = QLabel('Phase (degrees): 0.0')
        self.phase1Slider = QSlider(Qt.Horizontal)
        self.freq1Label = QLabel('Frequency (Hz): 0.0')
        self.freq1Slider = QSlider(Qt.Horizontal)
        self.phi2Label = QLabel('Phase (degrees): 0.0')
        self.phase2Slider = QSlider(Qt.Horizontal)
        self.freq2Label = QLabel('Frequency (Hz): 0.0')
        self.freq2Slider = QSlider(Qt.Horizontal)
        self.resetButton = QPushButton('RESET')
        self.fillCheckBox = QCheckBox('Add Fill')
        #
        self.createMenuBar()
        self.createDockWindows()
        self.updatePlot1()
        self.updatePlot2()
        self.updatePlotSum()

    def createMenuBar(self):
        # file menu actions:
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.triggered.connect(self.close)
        # create instance of menuBar
        menubar = self.menuBar()
        # add file menu and file menu actions
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def createDockWindows(self):
        controlPanelDockWidget = QDockWidget('controls', self)
        controlPanelDockWidget.setObjectName('ControlPanelDockWidget')
        controlPanelDockWidget.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea | Qt.LeftDockWidgetArea)
        # create a widget to house checkbox and list widget with QVBoxLayout
        houseWidget = QWidget(self) # self?
        # add a slider for phase
        layout = QVBoxLayout()
        #
        # Plot 1 phase and frequency controls
        layout.addWidget(self.phi1Label)
        self.phase1Slider.setRange(-180, 180)
        self.phase1Slider.setValue(self.phi1)
        QObject.connect(self.phase1Slider, SIGNAL('valueChanged(int)'), self.changePhi1)
        QObject.connect(self.phase1Slider, SIGNAL('valueChanged(int)'), self.updatePlot1)
        QObject.connect(self.phase1Slider, SIGNAL('valueChanged(int)'), self.updatePlotSum)
        layout.addWidget(self.phase1Slider)
        #
        layout.addWidget(self.freq1Label)
        self.freq1Slider.setRange(0, 100)
        self.freq1Slider.setValue(self.freq1)
        QObject.connect(self.freq1Slider, SIGNAL('valueChanged(int)'), self.changeFreq1)
        QObject.connect(self.freq1Slider, SIGNAL('valueChanged(int)'), self.updatePlot1)
        QObject.connect(self.freq1Slider, SIGNAL('valueChanged(int)'), self.updatePlotSum)
        layout.addWidget(self.freq1Slider)
        #
        # Plot 2 phase and frequency controls
        layout.addWidget(self.phi2Label)
        self.phase2Slider.setRange(-180, 180)
        self.phase2Slider.setValue(self.phi2)
        QObject.connect(self.phase2Slider, SIGNAL('valueChanged(int)'), self.changePhi2)
        QObject.connect(self.phase2Slider, SIGNAL('valueChanged(int)'), self.updatePlot2)
        QObject.connect(self.phase2Slider, SIGNAL('valueChanged(int)'), self.updatePlotSum)
        layout.addWidget(self.phase2Slider)
        #
        layout.addWidget(self.freq2Label)
        self.freq2Slider.setRange(0, 100)
        self.freq2Slider.setValue(self.freq2)
        QObject.connect(self.freq2Slider, SIGNAL('valueChanged(int)'), self.changeFreq2)
        QObject.connect(self.freq2Slider, SIGNAL('valueChanged(int)'), self.updatePlot2)
        QObject.connect(self.freq2Slider, SIGNAL('valueChanged(int)'), self.updatePlotSum)
        layout.addWidget(self.freq2Slider)
        #
        QObject.connect(self.resetButton, SIGNAL('clicked()'), self.resetValues)
        QObject.connect(self.resetButton, SIGNAL('clicked()'), self.updatePlot1)
        QObject.connect(self.resetButton, SIGNAL('clicked()'), self.updatePlot2)
        QObject.connect(self.resetButton, SIGNAL('clicked()'), self.updatePlotSum)
        layout.addWidget(self.resetButton)
        #
        QObject.connect(self.fillCheckBox, SIGNAL('stateChanged(int)'), self.updatePlot1)
        QObject.connect(self.fillCheckBox, SIGNAL('stateChanged(int)'), self.updatePlot2)
        QObject.connect(self.fillCheckBox, SIGNAL('stateChanged(int)'), self.updatePlotSum)
        layout.addWidget(self.fillCheckBox)
        #
        houseWidget.setLayout(layout)
        controlPanelDockWidget.setWidget(houseWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, controlPanelDockWidget)



    def changePhi1(self, value):
        self.phi1 = value * np.pi / 180
        self.phi1Label.setText('f(t) Phase (degrees): ' + str(value))

    def changeFreq1(self, value):
        self.freq1 = value
        self.freq1Label.setText('f(t) Frequency (Hz): ' + str(value))

    def changePhi2(self, value):
        self.phi2 = value * np.pi / 180
        self.phi2Label.setText('g(t) Phase (degrees): ' + str(value))

    def changeFreq2(self, value):
        self.freq2 = value
        self.freq2Label.setText('g(t) Frequency (Hz): ' + str(value))

    def resetValues(self):
        self.changePhi1(0.0)
        self.changeFreq1(0.0)
        self.phase1Slider.setValue(0.0)
        self.freq1Slider.setValue(0.0)
        self.changePhi2(0.0)
        self.changeFreq2(0.0)
        self.phase2Slider.setValue(0.0)
        self.freq2Slider.setValue(0.0)

    @pyqtSlot()  # I'm still not sure how to properly use static methods
    def updatePlot1(self):
        # Clear plot
        self.p1.clear()
        #t = np.linspace(0.0, 1.0, num=1000, endpoint=True)
        self.curve1 = np.cos(2*np.pi*self.freq1*self.t+self.phi1)
        c1 = pg.PlotCurveItem(pen='k')
        self.p1.addItem(c1)
        c1.setData(self.t, self.curve1)
        if self.fillCheckBox.isChecked():
            c1.setBrush('k')
            c1.setFillLevel(0.0)

    @pyqtSlot()
    def updatePlot2(self):
        # Clear plot
        self.p2.clear()
        #t = np.linspace(0.0, 1.0, num=1000, endpoint=True)
        self.curve2 = np.cos(2*np.pi*self.freq2*self.t+self.phi2)
        c2 = pg.PlotCurveItem(pen='k')
        self.p2.addItem(c2)
        c2.setData(self.t, self.curve2)
        if self.fillCheckBox.isChecked():
            c2.setBrush('k')
            c2.setFillLevel(0.0)

    @pyqtSlot()
    def updatePlotSum(self):
        # Clear plot
        self.pSum.clear()
        #t = np.linspace(0.0, 1.0, num=1000, endpoint=True)
        curveSum = self.curve1 + self.curve2
        cS = pg.PlotCurveItem(pen='k')
        self.pSum.addItem(cS)
        cS.setData(self.t, curveSum)
        if self.fillCheckBox.isChecked():
            cS.setBrush('k')
            cS.setFillLevel(0.0)


# =============== END OF SCRIPT =================
