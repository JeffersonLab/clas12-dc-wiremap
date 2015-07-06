
# coding: utf-8

# In[ ]:

import numpy as np
from os import path
import sys
sys.path.append('/home/goetz/local/src/clas12-dc-wiremap')
from clas12_wiremap import *

session = initialize_session()
dc_fill_tables(session)


# In[4]:

Crate = CalibrationDCHVCrate
SupplyBoard = CalibrationDCHVSupplyBoard
Subslot = CalibrationDCHVSubslot
Doublet = CalibrationDCHVDoublet
DoubletPin = CalibrationDCHVDoubletPin
DoubletPinMap = CalibrationDCHVDoubletPinMap
TransBoard = CalibrationDCHVTranslationBoard
Wire = CalibrationDCWire
SignalCable = CalibrationDCSignalCable
ReadoutConnector = CalibrationDCSignalReadoutConnector


# In[34]:

q = session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
       Crate.id)\
.join(Subslot,Doublet,TransBoard,SupplyBoard,Crate)\
.filter(
    SupplyBoard.wire_type == 'sense',
    Wire.wire >= TransBoard.wire_offset,
    Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)\
.order_by(
    Wire.sector,
    Wire.superlayer,
    Wire.layer,
    Wire.wire)

count = 0
for r in q:
    print(r)
    count += 1
    if count > 10:
        break
print(np.array(q.all()).shape)
print(np.array(q.all()).T.shape)
crate = np.array(q.all()).T[4]
print(crate.shape)
crate = crate.reshape((6,6,6,112))
print(crate.shape)
print(sum(crate == 2))


# In[29]:

from matplotlib import pyplot


# In[40]:

sel = crate==2
sel.shape
pyplot.imshow(crate[1][2][sel[1][2]])

