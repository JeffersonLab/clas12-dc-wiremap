from __future__ import print_function, division, unicode_literals

import sys
import os

from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore, uic
else:
    from PyQt4 import QtGui, QtCore, uic

from mpl import MplCanvasStatic

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('MainWindow.ui',self)

        #creating an instance of each object
        self.mpl = MplCanvasStatic()

        mpl_vbox = QtGui.QVBoxLayout()
        mpl_vbox.addWidget(self.mpl)
        mpl_vbox.addStretch(1)
        self.mpl_widget.setLayout(mpl_vbox)

        self.show()
        self.updating = False

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
