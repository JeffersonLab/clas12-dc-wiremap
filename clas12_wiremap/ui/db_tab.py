from __future__ import print_function, division

from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class DBTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        uic.loadUi('DBTab.ui', self)
    def get_buttons(self):               
                 
        fmt = 'sl{super_layer}_{direction}_{doublet}'
        
        buttons = []
        for sector in [5]:
            for super_layer in range(1,7):
         
                d_buttons = []
                for direction in ['f','b']:
                    
                                           
                    db_buttons = []
                    for doublet in range(1,7):
                            
                        opts = {
                                'super_layer' : super_layer,
                                'direction' : direction,
                                'doublet' : doublet}
                        b = getattr(self,fmt.format(**opts))
                            
                        db_buttons += [b.isChecked()]               
                    d_buttons += [db_buttons]
                buttons += [d_buttons]
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
        self.trial = DBTab()
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

                
        
