from __future__ import print_function, division

import os

from clas12_wiremap.ui import QtGui, uic
from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class DoubletPinTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        self.init_ui()
        #self.init_signals()
    '''
    def init_signals(self):
        for sec_id in range(6):
            for slyr_id,slyr in enumerate(self.superlayer[sec_id]):

                def _slyr(_,slyr=slyr,boxes=box):
                    checked = any([b.isChecked() for b in boxes])
                    slyr.setChecked(checked)

                for box_id, box in enumerate(self.box[sec_id][slyr_id]):

                    def _box(_,box=box,quads=quad):
                        slyr.clicked.connect(box.setChecked)
                        box.clicked.connect(_slyr)

                    for quad_id, quad in enumerate(self.quad[sec_id][slyr_id][box_id]):
                        for doublet_id, doublet in enumerate(self.doublet[sec_id][slyr_id][box_id][quad_id]):
                            for pin_id, pin in enumerate(self.pin[sec_id][slyr_id][box_id][quad_id][doublet_id]):
                                pass
                                '''

    def init_ui(self):

        self.superlayer = []
        self.box = []
        self.quad = []
        self.doublet = []
        self.pin = []


        for sec in range(6):
            sector_tab = QtGui.QTabWidget()
            sector_layout = QtGui.QHBoxLayout()
            sector_tab.setLayout(sector_layout)

            self.superlayer.append([])
            self.box.append([])
            self.quad.append([])
            self.doublet.append([])
            self.pin.append([])

            for slyr in range(6):
                superlayer_tab = QtGui.QWidget()
                superlayer_layout = QtGui.QGridLayout()

                # sector/superlayer
                superlayer_button = QtGui.QPushButton('Sector {}, Superlayer {}'.format(sec+1,slyr+1))

                self.superlayer[-1].append(superlayer_button)
                self.box[-1].append([])
                self.quad[-1].append([])
                self.doublet[-1].append([])
                self.pin[-1].append([])

                superlayer_button.setCheckable(True)

                superlayer_layout.addWidget(superlayer_button, 0, 0, 1, 7)

                for b,box_name in enumerate(['Forward','Backward']):

                    # direction/box
                    box_button = QtGui.QPushButton(box_name)

                    box_button.setSizePolicy(QtGui.QSizePolicy.Minimum,
                                             QtGui.QSizePolicy.Preferred)

                    self.box[-1][-1].append(box_button)
                    self.quad[-1][-1].append([])
                    self.doublet[-1][-1].append([])
                    self.pin[-1][-1].append([])

                    box_button.setCheckable(True)

                    superlayer_layout.addWidget(box_button,5*b+1,0,5,1)


                    for q in range(3):

                        # quad
                        quad_button = QtGui.QPushButton('Quad {}'.format(q+1))

                        self.quad[-1][-1][-1].append(quad_button)
                        self.doublet[-1][-1][-1].append([])
                        self.pin[-1][-1][-1].append([])

                        quad_button.setCheckable(True)

                        superlayer_layout.addWidget(quad_button, 5*b+1, q*2+1, 1, 2)


                        for d in range(2):

                            # doublet
                            doublet_button = QtGui.QPushButton('Doublet {}'.format(d+1))

                            self.doublet[-1][-1][-1][-1].append(doublet_button)
                            self.pin[-1][-1][-1][-1].append([])

                            doublet_button.setCheckable(True)

                            superlayer_layout.addWidget(doublet_button, 5*b+2, q*2+d+1)

                            pin_grid_widget = QtGui.QWidget()
                            pin_layout = QtGui.QGridLayout()
                            for pin in range(9):
                                x = pin % 3
                                y = pin // 3

                                # pin
                                pin_button = QtGui.QRadioButton('')

                                self.pin[-1][-1][-1][-1][-1].append(pin_button)

                                pin_button.setCheckable(True)
                                pin_button.setAutoExclusive(False)

                                pin_layout.setContentsMargins(9,9,9,0)
                                pin_layout.addWidget(pin_button,y,x)
                            pin_grid_widget.setLayout(pin_layout)
                            superlayer_layout.addWidget(pin_grid_widget, 5*b+3, q*2+d+1)

                superlayer_layout.setRowStretch(11,1)
                superlayer_layout.setColumnStretch(7,1)

                sector_tab.addTab(superlayer_tab, 'Superlayer {}'.format(slyr+1))
                superlayer_tab.setLayout(superlayer_layout)
            self.addTab(sector_tab, 'Sector {}'.format(sec+1))

            #trying to signal in same function
            for sec_id in range(6):
                superlayer = self.superlayer[sec_id]
                for sl_id, sl in enumerate(superlayer):
                    box = self.box[sec_id][sl_id]
                    def _sl(_,sl=sl, bxs=box):
                        checked = any([b.isChecked() for b in bx])
                        sl.setChecked(checked)
                    for bx_id,bx in enumerate(box):
                        sl.clicked.connect(bx.setChecked)
                        bx.clicked.connect(_sl)

                        quad = self.quad[sec_id][sl_id][bx_id]
                        def _bx(_,bx=bx, qs=quad):
                            checked = any([b.isChecked() for q in qs])
                            sl.setChecked(checked)

                        for q_id,q in enumerate(quad):
                            bx.clicked.connect(q.setChecked)
                            sl.clicked.connect(q.setChecked)
                            q.clicked.connect(_bx)
                            q.clicked.connect(_sl)

                            doublet = self.doublet[sec_id][sl_id][bx_id][q_id]
                            def _q(_,q=q, dbs=doublet):
                                checked = any([d.isChecked() for d in dbs])
                                q.setChecked(checked)

                            for d_id, d in enumerate(doublet):
                                q.clicked.connect(d.setChecked)
                                bx.clicked.connect(d.setChecked)
                                sl.clicked.connect(d.setChecked)
                                d.clicked.connect(_q)
                                d.clicked.connect(_bx)
                                d.clicked.connect(_sl)

                                pin = self.pin[sec_id][sl_id][bx_id][q_id][d_id]
                                def _d(_,d=d, pns=pin):
                                    checked = any([p.isChecked() for p in pns])
                                    d.setChecked(checked)

                                for p in pin:
                                    d.clicked.connect(p.setChecked)
                                    q.clicked.connect(p.setChecked)
                                    bx.clicked.connect(p.setChecked)
                                    sl.clicked.connect(p.setChecked)
                                    p.clicked.connect(_d)
                                    p.clicked.connect(_q)
                                    p.clicked.connect(_bx)
                                    p.clicked.connect(_sl)




if __name__ == '__main__':
    import sys

    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()

            self.dpin_tab = DoubletPinTab()
            self.setCentralWidget(self.dpin_tab)

            self.show()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


