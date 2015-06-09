from __future__ import print_function, division, unicode_literals

import sys

#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure

from clas12_wiremap.ui import QtGui, MainWindow

app = QtGui.QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
