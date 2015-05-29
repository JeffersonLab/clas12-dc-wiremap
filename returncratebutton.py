from __future__ import print_function, division

from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class CrateTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        uic.loadUi('CrateTab.ui', self)
    def get_buttons(self):               
                 
        fmt = 'SB{supply_board}_subslot{subslot}_{channel}'
        
        buttons = []
        for crate in [1]:
            for supply_board in range(1,6):
         
                if supply_board < 5:
                    subslots = range(1,4)
                else:
                    subslots = range(1,7)
                    
                ss_buttons = []
                for subslot in subslots:
                    
                    ch_buttons = []
                    for channel in range(1,9):
                        opts = {
                            'supply_board' : supply_board,
                            'subslot' : subslot,
                            'channel' : channel}
                        b = getattr(self,fmt.format(**opts))
                        
                        ch_buttons += [b.isChecked()]
                    ss_buttons += [ch_buttons]
                buttons += [ss_buttons]
        return buttons
        
    def status_changed(self):
        buttons = self.get_buttons()
                        
        print(buttons)
        #print('SB1,SS2,CH3:',buttons[0][1][2])
        
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.central_widget)

        hbox = QtGui.QHBoxLayout()
        self.trial = CrateTab()
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
        
