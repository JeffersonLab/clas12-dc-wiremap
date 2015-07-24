import sys
import math

import numpy as np
import scipy as sp

from numpy import ma
from numpy import random as rand
from scipy import special
from scipy import stats
from scipy import integrate
from scipy import optimize as opt
from scipy import interpolate as interp

from matplotlib import pyplot
from matplotlib import cm
from matplotlib.colors import LogNorm

sys.path.append('/home/goetz/local/src/clas12-dc-wiremap')
from clas12_wiremap import DCWires,plot_wiremap

reference_data = np.load('1.npy')
data = np.load('2.npy')

data[2,2,...,8:16] = 0
diff = (data - reference_data).ravel()
sel = np.abs(diff - diff.mean()) > 2*diff.std()
masked_diff = ma.masked_where(~sel,diff)



class Cursor:
    def __init__(self, ax, dcwires):
        self.ax = ax
        self.dcwires = dcwires

        # text location in axes coords
        self.txt = ax.text( 0.98, 0.98, '',
            ha = 'right',
            va = 'top',
            bbox = dict(alpha=0.6, color='white'),
            transform=ax.figure.transFigure,
            family='monospace')
        self.msg = '''\
Sec: {sec: >1}, Slyr: {slyr: >1}, Lyr: {lyr: >1}, Wire: {wire: >3}
Crate: {crate: >1}, Slot: {slot: >2}, Subslot: {subslot: >1}, Channel: {ch: >2}
Distr Board: {dboard: <8}, Quad: {quad: >1}, Doublet: {doublet: >1}
Trans Board: {tboard: >1}, Trans Board Half: {tboard_half: >1}'''

    def mouse_move(self, event):
        if not event.inaxes: return
        x, y = math.floor(event.xdata),math.floor(event.ydata+0.5)
        wire = x%112
        lyr = (y-1)%6 if y>0 else abs(y)%6
        slyr = ((y-1)//6) if y>0 else (y//-6)
        sec = (x//112) + (0 if y>0 else 3)
        point = (sec,slyr,lyr,wire)
        msgopts = dict(
            sec=sec+1,slyr=slyr+1,lyr=lyr+1,wire=wire+1,
            crate = self.dcwires.crate_id[point]+1,
            slot = self.dcwires.slot_id[point]+1,
            subslot = self.dcwires.subslot_id[point]+1,
            ch = self.dcwires.subslot_channel_id[point]+1,
            dboard = self.dcwires.distr_box_type[point],
            quad = self.dcwires.quad_id[point]+1,
            doublet = self.dcwires.doublet_id[point]+1,
            tboard = self.dcwires.trans_board_id[point]+1,
            tboard_half = self.dcwires.trans_board_slot_id[point]+1,
        )
        self.txt.set_text(self.msg.format(**msgopts))
        pyplot.draw()

dcwires = DCWires()
dcwires.fetch_data()

fig,ax = pyplot.subplots()
fig.subplots_adjust(top=.8)
pt,cb = plot_wiremap(ax, masked_diff, cbstyle=None)

cursor = Cursor(ax, dcwires)
pyplot.connect('motion_notify_event', cursor.mouse_move)


pyplot.show()
