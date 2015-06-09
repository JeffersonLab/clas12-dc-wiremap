from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore, uic
else:
    from PyQt4 import QtGui, QtCore, uic

from .sidebar import Sidebar
from .crate_tab import CrateTab
from .db_tab import DBTab
from .tb_tab import TBTab

from .main_window import MainWindow
