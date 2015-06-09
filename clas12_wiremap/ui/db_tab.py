from __future__ import print_function, division

import os
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore, uic
else:
    from PyQt4 import QtGui, QtCore, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class DBTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        curdir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(curdir,'DBTab.ui'), self)



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


if __name__ == '__main__':
    import sys

    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()

            self.db_tab = DBTab()
            self.setCentralWidget(self.db_tab)

            self.show()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


