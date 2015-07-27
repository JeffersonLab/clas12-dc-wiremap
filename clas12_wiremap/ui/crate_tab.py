from __future__ import print_function, division

import os

from clas12_wiremap.ui import QtGui, uic
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
                ct.clicked.connect(self.stateChanged)
                sb.clicked.connect(_ct)

                subslots = self.subslots[ct_id][sb_id]
                def _sb(_,sb=sb,sss=subslots):
                    chkd = any([s.isChecked() for s in sss])
                    sb.setChecked(chkd)

                for ss_id,ss in enumerate(subslots):
                    sb.clicked.connect(ss.setChecked)
                    ct.clicked.connect(ss.setChecked)
                    sb.clicked.connect(self.stateChanged)
                    ct.clicked.connect(self.stateChanged)
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
                        ss.clicked.connect(self.stateChanged)
                        sb.clicked.connect(self.stateChanged)
                        ct.clicked.connect(self.stateChanged)
                        ch.clicked.connect(self.stateChanged)
                    
                        
                        
                        
                          
    def get_crate(self):

        fmt = 'crate{crate}'

        buttons = []
        for crate in range(1,5):
                          
            opts = {    'crate' : crate                             
                        }
            b = getattr(self,fmt.format(**opts)) 
            buttons += [b.isChecked()]

        return buttons   
        
                         
    def get_supply_board(self):

        fmt = 'crate{crate}_SB{supply_board}'

        buttons = []
        for crate in range(1,5):
                
            sb_buttons = []
            if crate in range(1,3):
                slots = range(1,6)
            else:
                slots = range(1, 11) 
            for supply_board in slots:                             
                    
                          
                opts = {    'crate' : crate,
                                'supply_board' : supply_board                               
                        }
                b = getattr(self,fmt.format(**opts))    
                    
                sb_buttons += [b.isChecked()]
            buttons += [sb_buttons]

        return buttons
                        
    def get_subslots(self):

        fmt = 'crate{crate}_SB{supply_board}_subslot{subslot}'

        buttons = []
        for crate in range(1,5):
                
            sb_buttons = []
            if crate in range(1,3):
                slots = range(1,6)
            else:
                slots = range(1, 11) 
            for supply_board in slots:

                ss_buttons = []
                if supply_board in range(1,5) or range(6,10):
                    subslots = range(1,4)
                else:
                    subslots = range(1,7)
                for subslot in subslots:
                        
                    
                          
                    opts = {    'crate' : crate,
                                'supply_board' : supply_board,
                                'subslot' : subslot
                                }
                    b = getattr(self,fmt.format(**opts))                       
                    ss_buttons += [b.isChecked()]
                sb_buttons += [ss_buttons]
            buttons += [sb_buttons]

        return buttons
                            
    def get_channels(self):

        fmt = 'crate{crate}_SB{supply_board}_subslot{subslot}_{channel}'

        buttons = []
        for crate in range(1,5):
                
            sb_buttons = []
            if crate in range(1,3):
                slots = range(1,6)
            else:
                slots = range(1, 11) 
            for supply_board in slots:

                ss_buttons = []
                if supply_board in range(1,5) or range(6,10):
                    subslots = range(1,4)
                else:
                    subslots = range(1,7)
                for subslot in subslots:
                        
                    ch_buttons = []                    
                    for channel in range(1,9):
                            
                        opts = {    'crate' : crate,
                                    'supply_board' : supply_board,
                                    'subslot' : subslot,
                                    'channel' : channel
                                    }
                        b = getattr(self,fmt.format(**opts))
                        ch_buttons += [b.isChecked()]
                    ss_buttons += [ch_buttons]
                sb_buttons += [ss_buttons]
            buttons += [sb_buttons]

        return buttons
                        
    


if __name__ == '__main__':
    import sys

    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()

            self.crate_tab = CrateTab()
            self.setCentralWidget(self.crate_tab)
            print(self.crate_tab.get_crate())

            self.show()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
