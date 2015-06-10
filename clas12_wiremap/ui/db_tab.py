from __future__ import print_function, division

import os

from clas12_wiremap.ui import QtGui, uic
from clas12_wiremap import initialize_session, dc_fill_tables, dc_find_connections

class DBTab(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__(parent)
        curdir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(curdir,'DBTab.ui'), self)
        
    def init_buttons(self):

        sector_fmt     = 'sc{sector}'
        superlayer_fmt = 'sc{sector}_sl{superlayer}'
        direction_fmt  = 'sc{sector}_{direction}' #f or b
        box_fmt        = 'sc{sector}_{direction}_b{box}'
        quad_fmt       = 'sc{sector}_{direction}_b{box}_q{quad}'
        slot_fmt       = 'sc{sector}_{direction}_b{box}_q{quad}_{slot}'
        
        self.sectors = []
        self.superlayers = []
        self.directions = []
        self.boxs = []
        self.quads = []
        self.slots = []
        
        for sector_id in range(1,7):
        
            fmt = dict(sector=sector_id)

            self.sectors.append(getattr(self,sector_fmt.format(**fmt)))
            self.directions.append([])
            self.boxs.append([])
            self.quads.appent([])
            self.slots.append([])
           
            #superlayers are their own category
            
            for direction_id in ['f','b'] :
                fmt.update(direction=direction_id)
                
                self.directions[-1].append(getattr(self,direction_fmt.format(**fmt)))
                self.boxs[-1].append([])
                self.quads[-1].append([])
                self.slots[-1].append([])
                
                box_ids = range(1,7)
                
                for box_id in box_ids:
                    fmt.update(box = box_id)
                    
                    self.boxs[-1][-1].append(getattr(self, box_fmt.format(**fmt)))
                    self.quads[-1][-1].append([])
                    self.slots[-1][-1].append([])
                    
                    quad_ids = range(1,4)
                    
                    for quad_id in quad_ids:
                        fmt.update(quad = quad_id)
                        
                        self.quads[-1][-1][-1].append(getattr(self,quad_fmt.format(**fmt)))
                        self.slots[-1][-1][-1].append([])
                        
                        for slot_id in [1,2]:
                            fmt.update(slot = slot_id)
                            
                            self.slots[-1][-1][-1][-1].append(getattr(self,slot_fmt.format(**fmt)))
                        
                
                
            
            
            
            
        
    def get_buttons(self):

        fmt = 'sl{super_layer}_{direction}_{doublet}'

        buttons = []
        for sector in [5]:
            for super_layer in range(1,7):

                d_buttons = []
                for direction in ['f','b']:


                    db_buttons = []
                    for doublet in range(1,7):

                        opts = {
                                'super_layer' : super_layer,
                                'direction' : direction,
                                'doublet' : doublet}
                        b = getattr(self,fmt.format(**opts))

                        db_buttons += [b.isChecked()]
                    d_buttons += [db_buttons]
                buttons += [d_buttons]
        return buttons

    def status_changed(self):

        buttons = self.get_buttons()
        print(buttons)


if __name__ == '__main__':
    import sys

    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()

            self.db_tab = DBTab()
            self.setCentralWidget(self.db_tab)

            self.show()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


