from __future__ import print_function, division

import os
from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class Sidebar(QtGui.QWidget):
    def __init__(self,parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        curdir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(curdir,'Sidebar.ui'), self)

    def update_parameters(self):
        pass



if __name__ == '__main__':
    import sys

    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()

            self.sidebar = Sidebar()
            self.setCentralWidget(self.sidebar)

            self.show()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
