from __future__ import print_function, division

from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class TBTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        uic.loadUi('TBTab.ui', self)
    def get_buttons(self):               
                 
        fmt = 'sl{super_layer}_tb{transition_board}_{half}'
        
        buttons = []
        for sector in [1]:
            for super_layer in range(1,7):
   
                tb_buttons = []
                for transition_board in range(1,8):
                    
			tbh_buttons = []
			if transition_board < 6:
				halfs = range(1,3)
			else:
				halfs = [1]
			for half in halfs:
		                opts = {
		                    'super_layer' : super_layer,
		                    'transition_board' : transition_board,
		                     'half' : half }
		                b = getattr(self,fmt.format(**opts))
		                
		                tbh_buttons += [b.isChecked()]
		            tb_buttons += [tbh_buttons]
		        buttons += [tb_buttons]
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

                
        
