'''
Simple Cosine Wave UI using PyQt4 and pyqtgraph
Copyright 2015 Anthony Torlucci
Distributed under the terms of the GNU General Public License (see gpl.txt for more information)

    This file is part of Simple LAS Curve Viewer.

    Simple Cosine Wave UI is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Simple Cosine Wave UI is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Simple Cosine Wave UI.  If not, see <http://www.gnu.org/licenses/>.
'''

__author__ = 'Anthony Torlucci'
__version__ = '0.0.1'

# import python standard modules
import sys

# import 3rd party libraries
from PyQt4.QtGui import QApplication

#import local python
import MainWindow



def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Simple Cosine Wave UI')
    window = MainWindow.Window()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()