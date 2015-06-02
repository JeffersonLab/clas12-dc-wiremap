from __future__ import print_function, division

from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class DBTab(QtGui.QTabWidget):
    def __init__(self,parent=None):
            super(QtGui.QTabWidget, self).__init__(parent)
            uic.loadUi('DBTab.ui',self)
            self.updating = False
            self.session = initialize_session()
    def update_parameters(self):
        if not self.updating:
            self.updating = True
   #slot called in qt designer         
            
    def get_boardbuttons(self, direction, board):               
                 
        if direction in ['Forward','Backward']:
         
            if direction == 'Forward' :
                if board in [1,2,3,4,5,6]:
                    print(board, "Forward:", self.get_forwardbutton(board))
                         
            else:
                if board in [1,2,3,4,5,6]:
                    print(board, "Backward:", self.get_backwardbutton(board))
    
    
            
    def get_forwardbutton(self, board):
        return getattr(self, 'fbox' + str(board))     
        
    

    def get_backwardbutton(self, board):
        return getattr(self, 'bbox' + str(board))   
        
        
        
                 
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.central_widget)

        hbox = QtGui.QHBoxLayout()
        self.db = DBTab()
        hbox.addWidget(self.db)
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

                

