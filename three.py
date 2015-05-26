from __future__ import print_function, division

from numpy import random as rand
from PyQt4 import QtGui, uic

def fn():
    return rand.randint(0,7)

class SidebarWid(QtGui.QWidget):
    def __init__(self,parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        uic.loadUi('Sidebar.ui',self)

    def update_parameters(self):
        pass

class DistrBoardsTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        uic.loadUi('dbtabwidget.ui',self)

# object constructor class
class CrateTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        uic.loadUi('CrateTab.ui', self)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('MainWindow.ui',self)

        #creating an instance of each object
        self.sidebar = SidebarWid()
        self.distr_board = DistrBoardsTab()
        self.crate = CrateTab()

        sidebar_vbox = QtGui.QVBoxLayout()
        sidebar_vbox.addWidget(self.sidebar)
        sidebar_vbox.addStretch(1)
        self.sidebar_holder.setLayout(sidebar_vbox)

        distr_board_vbox = QtGui.QVBoxLayout()
        distr_board_vbox.addWidget(self.distr_board)
        distr_board_vbox.addStretch(1)
        self.distr_board_tab_holder.setLayout(distr_board_vbox)

        crate_vbox = QtGui.QVBoxLayout()
        crate_vbox.addWidget(self.crate)
        crate_vbox.addStretch(1)
        self.crate_tab_holder.setLayout(crate_vbox)

        self.show()
        self.updating = False

    def update_parameters(self):
        if not self.updating:
            self.updating = True
            self.updating = False

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
