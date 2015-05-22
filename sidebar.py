from __future__ import print_function, division

from PyQt4 import QtGui, uic

from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class Sidebar(QtGui.QWidget):
    def __init__(self,parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        uic.loadUi('Sidebar.ui',self)
        self.updating = False
        self.session = initialize_session()
        dc_fill_tables(self.session)

    def update_parameters(self):
        if not self.updating:
            self.updating = True

            attrs = ['wire_type','sector','superlayer','layer','wire',
                     'crate','supply_board','subslot','distr_box_type',
                     'quad','doublet','trans_board','trans_slot',]

            opts = dict(
                wire_type = ['any','sense','field'],
                distr_box_type = ['any','forward','backward'],)

            parms = {}
            for a in attrs:
                attr = getattr(self,a)
                attr_fixed = getattr(self,a+'_fixed')
                if attr_fixed.isChecked():
                    if isinstance(attr,QtGui.QSpinBox):
                        if attr.value() > 0:
                            parms[a] = attr.value() - 1
                    elif isinstance(attr,QtGui.QComboBox):
                        if attr.currentIndex() > 0:
                            parms[a] =  str(attr.currentText()).lower()

            fixed, nopts = dc_find_connections(self.session, **parms)

            for k in fixed:
                attr = getattr(self,k,None)
                if attr is not None:
                    was_blocked = attr.signalsBlocked()
                    attr.blockSignals(True)
                    if isinstance(attr,QtGui.QSpinBox):
                        attr.setValue(fixed[k]+1)
                    elif isinstance(attr,QtGui.QComboBox):
                        attr.setCurrentIndex(opts[k].index(fixed[k]))
                    attr.blockSignals(was_blocked)
                    getattr(self,k+'_nopts').setText('')
            for k in nopts:
                attr_fixed = getattr(self,k+'_fixed',None)
                if attr_fixed is not None:
                    getattr(self,k+'_nopts').setText(str(nopts[k]))
                    if not attr_fixed.isChecked():
                        attr = getattr(self,k,None)
                        if isinstance(attr,QtGui.QSpinBox):
                            getattr(self,k).setValue(0)
                        elif isinstance(attr,QtGui.QComboBox):
                            getattr(self,k).setCurrentIndex(0)

            self.updating = False


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.central_widget)

        hbox = QtGui.QHBoxLayout()
        self.sidebar = Sidebar()
        hbox.addWidget(self.sidebar)
        hbox.addStretch(1)

        vbox = QtGui.QVBoxLayout(self.central_widget)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.show()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
