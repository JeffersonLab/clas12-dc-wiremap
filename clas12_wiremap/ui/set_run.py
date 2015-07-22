from __future__ import print_function, division

import os

from clas12_wiremap.ui import QtGui, uic
from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections


class SetRunDialogue(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        curdir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(curdir,'SetRun.ui'), self)
        
    
    @staticmethod
    def getRunNum(parent = None):
        dialog = SetRunDialogue(parent)
        result = dialog.exec_()
        answer = dialog.spinBox.value()
        return (answer, result == QtGui.QDialog.Accepted)
        
if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    run,ok = SetRunDialogue.getRunNum()
    if ok:
        print('got run: '+str(run))        
    else:
        print('user canceled.')
    
   
