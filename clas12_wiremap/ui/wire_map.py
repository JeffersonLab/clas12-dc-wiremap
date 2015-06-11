import numpy as np
from numpy import random as rand

from clas12_wiremap.ui import QtGui

from matplotlib import pyplot, gridspec
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class WireMap(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = pyplot.figure(1, (18,8))

        data = rand.uniform(0,100,(36,6,112))

        self.axs = []
        self.pts = []

        sector_grid = gridspec.GridSpec(2,3,wspace=0.3,hspace=0.3)
        for sec in range(6):
            slyr_grid = gridspec.GridSpecFromSubplotSpec(6,1,
                wspace=0.0,hspace=0.1,
                subplot_spec=sector_grid[sec])

            for slyr in range(6):

                self.axs += [self.fig.add_subplot(slyr_grid[slyr])]
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

                # We want the axes cleared every time plot() is called
                ax.hold(False)

        super(WireMap,self).__init__(self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def change_data(self):
        data = rand.uniform(0,100,(36,6,112))
        for sec in range(6):
            for slyr in range(6):
                i = sec*6 + slyr
                pt = self.pts[i]
                pt.set_data(data[i])

if __name__ == '__main__':
    import sys

    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()

            self.wire_map = WireMap()
            self.setCentralWidget(self.wire_map)

            self.show()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


