from __future__ import print_function, division

import os
from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class TBTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        curdir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(curdir,'TBTab.ui'), self)



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

if __name__ == '__main__':
    import sys

    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()

            self.tb_tab = TBTab()
            self.setCentralWidget(self.tb_tab)

            self.show()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


