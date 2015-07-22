from __future__ import print_function, division

import os

from clas12_wiremap.ui import QtGui, uic
from clas12_wiremap.ui import Sidebar, CrateTab, DBTab, TBTab, WireMaps, SetRunDialogue
from clas12_wiremap.ui.dcrb_tab import DCRB
from clas12_wiremap.ui.stb_tab import STBTab
from clas12_wiremap import initialize_session, DCWires

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        curdir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(curdir,'MainWindow.ui'), self)
        self.dcwires = DCWires()
        #self.dcwires.initialize_session()



        #self.run_number.setValue(int(DCWires.runnum))
        #self.run_number.valueChanged.connect(self.run_number.show)

        #if (self.run_number.value.Changed() :
            #print(self.run_number.value())


        ### Explorer Tabs
        self.explorer_tabs = QtGui.QTabWidget()

        self.crate = CrateTab()
        self.crate.setMinimumWidth(750)
        self.crate.setMaximumHeight(1000)
        crate_vbox = QtGui.QVBoxLayout(self.crate)
        self.explorer_tabs.addTab(self.crate, 'Crates')


        self.dboard = DBTab()
        self.dboard.setMinimumWidth(750)
        dboard_vbox = QtGui.QVBoxLayout(self.dboard)
        self.explorer_tabs.addTab(self.dboard, 'Distribution Boards')

        self.tboard = TBTab()
        self.tboard.setMinimumWidth(750)
        tboard_vbox = QtGui.QVBoxLayout(self.tboard)
        self.explorer_tabs.addTab(self.tboard, 'Translation Boards')

        self.dcrb = DCRB()
        self.dcrb.setMinimumWidth(750)
        dcrb_vbox = QtGui.QVBoxLayout(self.dcrb)
        self.explorer_tabs.addTab(self.dcrb, 'Drift Chamber Readout Board')

        self.stb = STBTab()
        self.stb.setMinimumWidth(750)
        stb_vbox = QtGui.QVBoxLayout(self.stb)
        self.explorer_tabs.addTab(self.stb, 'Signal Translation Board')

        self.explorer_tabs.setMinimumWidth(750)
        self.explorer_tabs.setSizePolicy(
                                   QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Expanding)


        explorer_vbox = QtGui.QVBoxLayout()
        explorer_vbox.addWidget(self.explorer_tabs)
        self.explorer_holder.setLayout(explorer_vbox)

        ### Chooser Sidebar
        #self.sidebar = Sidebar(self.session)
        #sidebar_vbox = QtGui.QVBoxLayout()
        #sidebar_vbox.addWidget(self.sidebar)
        #self.chooser_holder.setLayout(sidebar_vbox)

        ### Wiremap
        self.wiremaps = WireMaps()
        wmap_vbox = QtGui.QVBoxLayout()
        wmap_vbox.addWidget(self.wiremaps)
        self.wiremap_holder.setLayout(wmap_vbox)

        def update_wiremap(sec,data):
            if sec is not None:
                self.wiremaps.setCurrentIndex(sec+1)
            else:
                self.wiremaps.setCurrentIndex(0)
            self.wiremaps.data = data

        #self.sidebar.post_update = update_wiremap

        self.setModeExplorer()
        self.show()

    def setModeExplorer(self):
        self.actionExplorer.setChecked(True)
        self.actionChooser.setChecked(False)
        self.left_stacked_widget.setCurrentIndex(0)

    def setModeChooser(self):
        self.actionExplorer.setChecked(False)
        self.actionChooser.setChecked(True)
        self.left_stacked_widget.setCurrentIndex(1)

    def setRunDialogue(self):
        run,ok = SetRunDialogue.getRunNum()
        if ok:
            self.loadRun(run)




    def loadRun(self, runnumber):
        self.rundisplay.setNum(runnumber)
        self.dcwires.run = runnumber
        self.dcwires.fetch_data()







if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    #palette    = QtGui.QPalette()
    #palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap("grass.jpg")))
    #main_window.setPalette(palette)
    sys.exit(app.exec_())
