import numpy as np
from numpy import random as rand

from clas12_wiremap.ui import QtGui

from matplotlib import pyplot, gridspec, cm
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT \
    as NavigationToolbar
from matplotlib.figure import Figure
from component_array import*


class WireMap(QtGui.QWidget):

    def __init__(self, parent=None):
        super(WireMap,self).__init__(parent)
        self.parent = parent

        self.setup_widgets()

        self.vbox = QtGui.QVBoxLayout(self)
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.toolbar)

    def setup_widgets(self):
        # setting up dimensions
        self.fig = Figure((5.0, 4.0), dpi=100)
        #attaching the figure to the canvas
        self.canvas = FigureCanvas(self.fig)
        #attaching a toolbar to the canvas
        self.toolbar = NavigationToolbar(self.canvas, self.parent)

        self.axs = [[] for i in range(6)]
        self.pts = [[None]*6 for i in range(6)]

        sector_grid = gridspec.GridSpec(2,3,wspace=0.3,hspace=0.2)
        for sec in range(6):
            slyr_grid = gridspec.GridSpecFromSubplotSpec(6,1,
                wspace=0.0,hspace=0.1,
                subplot_spec=sector_grid[sec])
            for slyr in range(6):
                self.axs[sec].append(
                    self.fig.add_subplot(slyr_grid[5-slyr]))

    def update_plots(self):
        for sec in range(6):
            for slyr in range(6):
                self.pts[sec][slyr] = \
                    self.superlayer_plot(self.axs[sec][slyr],sec,slyr)
        self.canvas.draw()

    def superlayer_plot(self,ax,sec,slyr):
        if not hasattr(self,'data'):
            self.data = fetchCrateArray(session)
        pt = ax.imshow(self.data[sec][slyr],
            origin='lower',
            aspect='auto',
            interpolation='nearest',
            extent=[0.5,112.5,-0.5,5.5],
            vmin=0,
            cmap=cm.ocean)
        if slyr == 5:
            ax.set_title('Sector '+str(sec+1))
        if (sec > 2) and (slyr == 0):
            ax.xaxis.set_ticks([1]+list(range(32,113,32)))
            ax.xaxis.set_ticklabels([1]+list(range(32,113,32)))
        else:
            ax.xaxis.set_major_locator(pyplot.NullLocator())
        ax.set_ylabel(str(slyr+1))
        ax.yaxis.set_major_locator(pyplot.NullLocator())
        ax.hold(False)
        return pt



class WireMapSector(QtGui.QWidget):

    def __init__(self, sector, parent=None):
        super(WireMapSector,self).__init__(parent)
        self.sector = sector
        self.parent = parent

        self.setup_widgets()

        self.vbox = QtGui.QVBoxLayout(self)
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.toolbar)

    def setup_widgets(self):

        self.fig = Figure((5.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self.parent)

        self.axs = []
        self.pts = [None]*6

        slyr_grid = gridspec.GridSpec(6,1,wspace=0.0,hspace=0.1)
        for slyr in range(6):
            self.axs.append(
                self.fig.add_subplot(slyr_grid[5-slyr]))

    def update_plots(self):
        for slyr in range(6):
            self.pts[slyr] = \
                self.superlayer_plot(self.axs[slyr],slyr)
        self.canvas.draw()

    def superlayer_plot(self,ax,slyr):
        if not hasattr(self,'data'):
            self.data = fetchCrateArray(session)
        pt = ax.imshow(self.data[slyr],
            origin='lower',
            aspect='auto',
            interpolation='nearest',
            extent=[0.5,112.5,-0.5,5.5],
            vmin=0,
            cmap=cm.ocean)
        if slyr == 5:
            ax.set_title('Sector '+str(self.sector+1))
        if slyr == 0:
            ax.xaxis.set_ticks([1]+list(range(32,113,32)))
            ax.xaxis.set_ticklabels([1]+list(range(32,113,32)))
        else:
            ax.xaxis.set_major_locator(pyplot.NullLocator())
        ax.set_ylabel(str(slyr+1))
        ax.yaxis.set_major_locator(pyplot.NullLocator())
        ax.hold(False)
        return pt


class WireMaps(QtGui.QStackedWidget):

    def __init__(self, parent=None):
        super(WireMaps,self).__init__(parent)

        self.wiremap = WireMap(self)
        self.addWidget(self.wiremap)

        self.sec_wiremaps = []
        for sec in range(6):
            self.sec_wiremaps.append(WireMapSector(sec,self))
            self.addWidget(self.sec_wiremaps[sec])

        self.data = fetchCrateArray(session)

    @property
    def data(self):
        return self.wiremap.data

    @data.setter
    def data(self,d):
        self._data = d

        self.wiremap.data = self._data
        for sec in range(6):
            self.sec_wiremaps[sec].data = self._data[sec]

        self.update_active_plots()

    def update_active_plots(self):
        if super(WireMaps,self).currentIndex() == 0:
            self.wiremap.update_plots()
        else:
            sec = super(WireMaps,self).currentIndex() - 1
            self.sec_wiremaps[sec].update_plots()

    def setCurrentIndex(self,*args,**kwargs):
        super(WireMaps,self).setCurrentIndex(*args,**kwargs)
        self.update_active_plots()

if __name__ == '__main__':
    import sys
    from matplotlib import pyplot
    session = initialize_session()
    dc_fill_tables(session)

    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()

            wid = QtGui.QWidget()
            vbox = QtGui.QVBoxLayout()
            wid.setLayout(vbox)

            cbox = QtGui.QSpinBox()
            cbox.setMinimum(0)
            cbox.setMaximum(6)
            cbox.setSpecialValueText('-')
            stack = WireMaps()
            #stack.data = fetchCrateArray(session)
            #stack.data = fetchSubslotArray(session)
            #stack.data = fetchSignalCableArray(session)
            stack.data = fetchCrateArray(session)



            vbox.addWidget(cbox)
            vbox.addWidget(stack)

            self.setCentralWidget(wid)

            cbox.valueChanged.connect(stack.setCurrentIndex)

            self.show()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


