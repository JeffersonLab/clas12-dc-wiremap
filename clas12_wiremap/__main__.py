from __future__ import print_function, division, unicode_literals

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

import sys
import os
import random
from numpy import arange, sin, pi
from numpy import random as rand

from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from dc_tables import initialize_session
from dc_fill_tables import dc_fill_tables
from dc_queries import dc_find_connections

from ui import CrateTab, DBTab, TBTab, Sidebar

print('connecting to database...')
session = initialize_session()

print('filling tables...')
dc_fill_tables(session)

find_connections = lambda **kw: dc_find_connections(session,**kw)

parms = [
    dict(wire_type = 'sense'),
    dict(wire_type='sense',sector=0,superlayer=0,layer=0),
    dict(wire_type='sense',sector=0,superlayer=0,layer=0,wire=0),
]

print('making queries:')
for p in parms:
    print(p)
    print('   ',find_connections(**p))

print('timing queries...')

import timeit

setup = '''\
from dc_tables import initialize_session
from dc_fill_tables import dc_fill_tables
from dc_queries import dc_find_connections
session = initialize_session()
dc_fill_tables(session)'''
using_all = '''\
dc_find_connections.all = True
dc_find_connections(session)'''
using_one = '''\
dc_find_connections.all = False
dc_find_connections(session)'''

print('empty input')
res = timeit.timeit(using_all,setup,number=20)
print('  using all:',res)
res = timeit.timeit(using_one,setup,number=20)
print('  using one:',res)

using_all = '''\
dc_find_connections.all = True
dc_find_connections(session,wire_type='sense',sector=0,superlayer=0)'''
using_one = '''\
dc_find_connections.all = False
dc_find_connections(session,wire_type='sense',sector=0,superlayer=0)'''

print('partial input')
res = timeit.timeit(using_all,setup,number=20)
print('  using all:',res)
res = timeit.timeit(using_one,setup,number=20)
print('  using one:',res)

using_all = '''\
dc_find_connections.all = True
dc_find_connections(session,wire_type='sense',sector=0,superlayer=0,layer=0,wire=0)'''
using_one = '''\
dc_find_connections.all = False
dc_find_connections(session,wire_type='sense',sector=0,superlayer=0,layer=0,wire=0)'''

print('full input')
res = timeit.timeit(using_all,setup,number=20)
print('  using all:',res)
res = timeit.timeit(using_one,setup,number=20)
print('  using one:',res)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('MainWindow.ui',self)

        #creating an instance of each object
        self.sidebar = Sidebar()
        self.dboard = DBTab()
        self.crate = CrateTab()
        self.tboard = TBTab()

        #self.mpl = MplCanvasStatic()
        #mpl_vbox = QtGui.QVBoxLayout()
        #mpl_vbox.addWidget(self.mpl)
        #mpl_vbox.addStretch(1)
        #self.wire_tab_holder.setLayout(mpl_vbox)

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

app = QtGui.QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
