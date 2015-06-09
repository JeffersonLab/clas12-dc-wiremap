from __future__ import print_function, division

import os

from clas12_wiremap.ui import QtGui, uic
from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class TBTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        curdir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(curdir,'TBTab.ui'), self)
        
    def init_buttons(self):

        sc_fmt = 'sc{sector}'
        sl_fmt = 'sc{sector}_sl{superlyr}'
        b_fmt = 'sc{sector}_sl{superlyr}_b{board}'
        slot_fmt = 'sc{sector}_sl{superlyr}_b{board}_{slot}'

        self.sector = []
        self.superlyr = []
        self.board = []
        self.slot = []

        for sector_id in range(1,7):
            fmt = dict(sector=sector_id)

            self.sectors.append(getattr(self,sc_fmt.format(**fmt)))
            self.superlyrs.append([])
            self.boards.append([])
            self.slots.append([])
            
            sl_ids = range(1,7)

            for sl_id in sl_ids:
                fmt.update(superlyr=sl_id)

                self.superlyrs[-1].append(getattr(self,sl_fmt.format(**fmt)))
                self.boards[-1].append([])
                self.slots[-1].append([])

                b_ids = range(1,8)

                for b_id in b_ids:
                    fmt.update(board=b_id)

                    self.boards[-1][-1].append(getattr(self,ss_fmt.format(**fmt)))
                    self.slots[-1][-1].append([])
                    
                    if b_id < 6:
                        slot_id = range(1,3)
                    else :
                        slot_id = range(1,2)

                    for slotz_id in slot_id:
                        fmt.update(slot=slotz_id)

                        self.slots[-1][-1][-1].append(getattr(self,slot_fmt.format(**fmt)))

        for sc_id,sc in enumerate(self.sectors): 

            superlyrs = self.superlyrs[sc_id]
            def _sc(_,sc=sc,sls=superlyrs):
                slotkd = any([b.isChecked() for b in sls])
                sc.setChecked(slotkd)

            for sl_id,sl in enumerate(superlyrs):
                sc.clicked.connect(sl.setChecked)
                sl.clicked.connect(_sc)

                board = self.boards[sc_id][sl_id]
                def _sl(_,sl=sl,slotss=boards):
                    slotkd = any([s.isChecked() for s in slotss])
                    sl.setChecked(slotkd)

                for b_id,b in enumerate(board):
                    sl.clicked.connect(b.setChecked)
                    sc.clicked.connect(b.setChecked)
                    b.clicked.connect(_sl)
                    b.clicked.connect(_sc)

                    slotsss = self.channels[sc_id][sl_id][b_id]
                    def _b(_,b=b,slots=slotsss):
                        slotkd = any([c.isChecked() for c in slots])
                        b.setChecked(slotkd)

                    for ch in channels:
                        b.clicked.connect(slot.setChecked)
                        sl.clicked.connect(slot.setChecked)
                        sc.clicked.connect(slot.setChecked)
                        slot.clicked.connect(_b)
                        slot.clicked.connect(_sl)
                        slot.clicked.connect(_sc)

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


