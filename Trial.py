from __future__ import print_function, division

from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class Trial(QtGui.QWidget):
    def __init__(self,parent=None):
            super(QtGui.QWidget, self).__init__(parent)
            uic.loadUi('Trial.ui',self)
            self.updating = False
            self.session = initialize_session()
    def update_parameters(self):
        if not self.updating:
            self.updating = True
   #slot called in qt designer         
    def button_changed(self):
        for board in [2,3]:
            #loop over things to get
            print(board,":",self.get_button(board))
    #the actual getting of each element
    def get_button(self, board):
        return getattr(self, 'SB' + str(board))
                
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.central_widget)

        hbox = QtGui.QHBoxLayout()
        self.trial = Trial()
        hbox.addWidget(self.trial)
        hbox.addStretch(1)

        vbox = QtGui.QVBoxLayout(self.central_widget)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.show()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

                
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
