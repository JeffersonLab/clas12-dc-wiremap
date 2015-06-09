from __future__ import print_function, division, unicode_literals

import sys
import os
import random
import time
import numpy as np
from numpy import random as rand
from matplotlib import pyplot, gridspec, animation

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        super(MplCanvas,self).__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MplCanvasStatic(MplCanvas):
    
    def __init__(self,parent=None):
        super(MplCanvasStatic,self).__init__(parent)
        data = rand.uniform(0,100,(36,6,112))

        self.fig = pyplot.figure(1, (18,8))
        self.axs = []
        self.pts = []

        sector_grid = gridspec.GridSpec(2,3,wspace=0.3,hspace=0.3)
        for sec in range(6):
            slyr_grid = gridspec.GridSpecFromSubplotSpec(6,1,
                wspace=0.0,hspace=0.1,
                subplot_spec=sector_grid[sec])

            for slyr in range(6):

                self.axs += [fig.add_subplot(slyr_grid[slyr])]
                ax = self.axs[-1]

                self.pts += [ax.imshow(data[sec*6 + (5-slyr)],
                    origin='lower',
                    aspect='auto',
                    interpolation='nearest',
                    extent=[-0.5,111.5,-0.5,5.5])]
                if slyr == 0:
                    ax.set_title('Sector '+str(sec+1))
                ax.set_ylabel(str(6-slyr))
                ax.xaxis.set_major_locator(pyplot.NullLocator())
                ax.yaxis.set_major_locator(pyplot.NullLocator())


    def update(i):
        data = rand.uniform(0,100,(36,6,112))
        for sec in range(6):
            for slyr in range(6):
                i = sec*6 + slyr
                pt = self.pts[i]
                pt.set_data(data[i])


#ani = animation.FuncAnimation(fig, update, np.arange(1, 200),interval=1)
#pyplot.show()




