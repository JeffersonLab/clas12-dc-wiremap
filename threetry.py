from __future__ import print_function, division, unicode_literals

from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

import sys
import os
import random
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import random as rand
from PyQt4 import QtGui, uic
#fix file names
from db_tab import DBTab
from tb_tab import TBTab
from crate_tab import CrateTab
from sidebar_view import SidebarWid
from mpl_canvas import MplCanvasStatic

def fn():
    return rand.randint(0,7)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('MainWindow.ui',self)

        #creating an instance of each object
        self.sidebar = SidebarWid()
        self.dboard = DBTab()
        self.crate = CrateTab()
        self.tboard = TBTab()
        self.mpl = MplCanvasStatic()
        
        mpl_vbox = QtGui.QVBoxLayout()
        mpl_vbox.addWidget(self.mpl)
        mpl_vbox.addStretch(1)
        self.wire_tab_holder.setLayout(mpl_vbox)

        sidebar_vbox = QtGui.QVBoxLayout()
        sidebar_vbox.addWidget(self.sidebar)
        sidebar_vbox.addStretch(1)
        self.sidebar_holder.setLayout(sidebar_vbox)          

        dboard_vbox = QtGui.QVBoxLayout()
        dboard_vbox.addWidget(self.dboard)
        dboard_vbox.addStretch(1)
        self.distr_board_tab_holder.setLayout(dboard_vbox)
        
        tboard_vbox = QtGui.QVBoxLayout()
        tboard_vbox.addWidget(self.tboard)
        tboard_vbox.addStretch(1)
        self.trans_board_tab_holder.setLayout(tboard_vbox)

        crate_vbox = QtGui.QVBoxLayout()
        crate_vbox.addWidget(self.crate)
        crate_vbox.addStretch(1)
        self.crate_tab_holder.setLayout(crate_vbox)


        ct_fmt = 'crate{crate_num}'
        sb_fmt = 'crate{crate_num}_SB{supply_board}'
        ss_fmt = 'crate{crate_num}_SB{supply_board}_subslot{subslot}'
        ch_fmt = 'crate{crate_num}_SB{supply_board}_subslot{subslot}_{channel}'
        
        for crate_index in [1,2,3,4]:
            ct = getattr(self.crate,ct_fmt.format(crate_num=crate_index))
            for sb_index in [1,2,3,4,5]:
                sb = getattr(self.crate,sb_fmt.format(supply_board=sb_index)
                if sb_index < 5:
                    ss_indexes = [1,2,3]
                else:
                    ss_indexes = [1,2,3,4,5,6]
                for ss_index in ss_indexes:
                    ss = getattr(self.crate,ss_fmt.format(supply_board=sb_index,subslot=ss_index))
                    for ch_index in [1,2,3,4,5,6,7,8]:
                        ch = getattr(self.crate,ch_fmt.format(supply_board=sb_index,subslot=ss_index,channel=ch_index))
                        ss.clicked.connect(ch.setChecked)
                        sb.clicked.connect(ss.setChecked)
                        sb.clicked.connect(ch.setChecked)
                        ct.clicked.connect(sb.setChecked)
                        ct.clicked.connect(ss.setChecked)
                        ct.clicked.connect(ch.setChecked)
                        
                        #if ss is off and ch is clicked turn on ss(parent)
                        if ss.setChecked == False:
                            ch.clicked.connect(ss.setChecked)                            
                            #if sb is off and ss is clicked turn on sb(parent)
                            if sb.setChecked == False:
                                ss.clicked.connect(sb.setChecked)
                                #if ct is off and sb is clicked turn on ct(parent)
                                if ct.setChecked == False: 
                                    sb.clicked.connect(ct.setChecked)
                                    
                        #if sb is off and ss is clicked turn on sb(parent)
                        if sb.setChecked == False:
                            ss.clicked.connect(sb.setChecked)
                            #if ct is off and sb is clicked turn on ct(parent)
                            if ct.setChecked == False: 
                                sb.clicked.connect(ct.setChecked)
                            
                        #if ct is off and sb is clicked turn on ct(parent)
                        if ct.setChecked == False: 
                             sb.clicked.connect(ct.setChecked)

                        
            self.show()
            self.updating = False

    def update_parameters(self):
        if not self.updating:
            self.updating = True
            self.updating = False

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
