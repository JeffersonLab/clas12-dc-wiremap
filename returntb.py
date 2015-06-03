from __future__ import print_function, division

from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class TBTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        uic.loadUi('TBTab.ui', self)
    def get_buttons(self):               
                 
        fmt = 'sl{super_layer}_{board}'
        
        buttons = []
        for sector in [2]:
            for super_layer in range(1,7):
         
                b_buttons = []
                for board in range(1,13):
                    opts = {
                                'super_layer' : super_layer,
                                'board' : board}
                    b = getattr(self,fmt.format(**opts))
                    
                    b_buttons += [b.isChecked()]
                buttons += [b_buttons]      
         
        return buttons
        
    def status_changed(self):
        
        buttons = self.get_buttons()                        
        print(buttons)
    
        
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.central_widget)

        hbox = QtGui.QHBoxLayout()
        self.trial = TBTab()
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

                
        
