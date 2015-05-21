from __future__ import print_function, division

from numpy import random as rand
from PyQt4 import QtGui, uic

def fn():
    return rand.randint(0,7)

class Sidebar(QtGui.QWidget):
    def __init__(self,parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        uic.loadUi('Sidebar.ui',self)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('MainWindow.ui',self)

        self.sidebar = Sidebar(self.sidebar_holder)

        self.show()
        self.updating = False

    def update_parameters(self):
        if not self.updating:
            self.updating = True
            self.item1value.setValue(fn())
            self.item2value.setValue(fn())
            self.item1info.setText('fixed? '+str(fn()))
            self.item2info.setText('fixed? '+str(fn()))
            self.updating = False

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
