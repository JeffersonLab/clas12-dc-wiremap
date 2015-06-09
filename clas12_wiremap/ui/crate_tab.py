from __future__ import print_function, division

import os
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore, uic
else:
    from PyQt4 import QtGui, QtCore, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class CrateTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        curdir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(curdir,'CrateTab.ui'), self)
        self.init_buttons()

    def init_buttons(self):

        ct_fmt = 'crate{crate}'
        sb_fmt = 'crate{crate}_SB{supply_board}'
        ss_fmt = 'crate{crate}_SB{supply_board}_subslot{subslot}'
        ch_fmt = 'crate{crate}_SB{supply_board}_subslot{subslot}_{channel}'

        self.crates = []
        self.supply_boards = []
        self.subslots = []
        self.channels = []

        for crate_id in range(1,5):
            fmt = dict(crate=crate_id)

            self.crates.append(getattr(self,ct_fmt.format(**fmt)))
            self.supply_boards.append([])
            self.subslots.append([])
            self.channels.append([])

            if crate_id < 3:
                sb_ids = range(1,6)
            else:
                sb_ids = range(1,11)

            for sb_id in sb_ids:
                fmt.update(supply_board=sb_id)

                self.supply_boards[-1].append(getattr(self,sb_fmt.format(**fmt)))
                self.subslots[-1].append([])
                self.channels[-1].append([])

                if (sb_id % 5):
                    ss_ids = range(1,4)
                else:
                    ss_ids = range(1,7)

                for ss_id in ss_ids:
                    fmt.update(subslot=ss_id)

                    self.subslots[-1][-1].append(getattr(self,ss_fmt.format(**fmt)))
                    self.channels[-1][-1].append([])

                    for ch_id in range(1,9):
                        fmt.update(channel=ch_id)

                        self.channels[-1][-1][-1].append(getattr(self,ch_fmt.format(**fmt)))

        for ct_id,ct in enumerate(self.crates):

            supply_boards = self.supply_boards[ct_id]
            def _ct(_,ct=ct,sbs=supply_boards):
                chkd = any([b.isChecked() for b in sbs])
                ct.setChecked(chkd)

            for sb_id,sb in enumerate(supply_boards):
                ct.clicked.connect(sb.setChecked)
                sb.clicked.connect(_ct)

                subslots = self.subslots[ct_id][sb_id]
                def _sb(_,sb=sb,sss=subslots):
                    chkd = any([s.isChecked() for s in sss])
                    sb.setChecked(chkd)

                for ss_id,ss in enumerate(subslots):
                    sb.clicked.connect(ss.setChecked)
                    ct.clicked.connect(ss.setChecked)
                    ss.clicked.connect(_sb)
                    ss.clicked.connect(_ct)

                    channels = self.channels[ct_id][sb_id][ss_id]
                    def _ss(_,ss=ss,chs=channels):
                        chkd = any([c.isChecked() for c in chs])
                        ss.setChecked(chkd)

                    for ch in channels:
                        ss.clicked.connect(ch.setChecked)
                        sb.clicked.connect(ch.setChecked)
                        ct.clicked.connect(ch.setChecked)
                        ch.clicked.connect(_ss)
                        ch.clicked.connect(_sb)
                        ch.clicked.connect(_ct)



if __name__ == '__main__':
    import sys

    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()

            self.crate_tab = CrateTab()
            self.setCentralWidget(self.crate_tab)

            self.show()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
