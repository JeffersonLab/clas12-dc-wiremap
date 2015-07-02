import numpy as np
from os import path
import sys
sys.path.append('/home/bbyrd/clas12-dc-wiremap')
from clas12_wiremap import *



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
    

def fetchCrateArray(session):       

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

    crate = np.array(q.all()).T[4]
    return crate.reshape((6,6,6,112))
    
    
def fetchSupplyBoardArray(session):       

    q = session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
           SupplyBoard.id)\
    .join(Subslot,Doublet,TransBoard,SupplyBoard)\
    .filter(
        SupplyBoard.wire_type == 'sense',
        Wire.wire >= TransBoard.wire_offset,
        Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)\
    .order_by(
        Wire.sector,
        Wire.superlayer,
        Wire.layer,
        Wire.wire)

    supplyboard = np.array(q.all()).T[4]
    return supplyboard.reshape((6,6,6,112))
    
 

    
def fetchSubslotArray(session):
    q = session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
           Subslot.subslot_id)\
    .join(Subslot,Doublet,TransBoard, SupplyBoard)\
    .filter(
        SupplyBoard.wire_type == 'sense',
        Wire.wire >= TransBoard.wire_offset,
        Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)\
    .order_by(
        Wire.sector,
        Wire.superlayer,
        Wire.layer,
        Wire.wire)

    subslot = np.array(q.all()).T[4]
    return subslot.reshape((6,6,6,112))   

    
def fetchDoubletArray(session):
    q = session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
           Doublet.id)\
    .join(Subslot,Doublet,TransBoard, SupplyBoard)\
    .filter(
        SupplyBoard.wire_type == 'sense',
        Wire.wire >= TransBoard.wire_offset,
        Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)\
    .order_by(
        Wire.sector,
        Wire.superlayer,
        Wire.layer,
        Wire.wire)

    doublet = np.array(q.all()).T[4]
    return doublet.reshape((6,6,6,112))
       
def fetchDoubletPinArray(session):
    q = session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
           DoubletPin.id)\
    .join(Subslot,Doublet,TransBoard, SupplyBoard)\
    .filter(
        SupplyBoard.wire_type == 'sense',
        Wire.wire >= TransBoard.wire_offset,
        Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)\
    .order_by(
        Wire.sector,
        Wire.superlayer,
        Wire.layer,
        Wire.wire)

    doublet_pin = np.array(q.all()).T[4]
    return doublet_pin.reshape((6,6,6,112))   
    
 
    
def fetchDoubletPinMapArray(session):
    q = session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
           DoubletPinMap.id)\
    .join(Subslot,Doublet,TransBoard, SupplyBoard)\
    .filter(
        SupplyBoard.wire_type == 'sense',
        Wire.wire >= TransBoard.wire_offset,
        Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)\
    .order_by(
        Wire.sector,
        Wire.superlayer,
        Wire.layer,
        Wire.wire)

    doublet_pin_map = np.array(q.all()).T[4]
    return doublet_pin_map.reshape((6,6,6,112))
    

def fetchTransBoard(session):
    q = session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
           TransBoard.board_id, TransBoard.slot_id)\
    .join(Subslot,Doublet,TransBoard, SupplyBoard)\
    .filter(
        SupplyBoard.wire_type == 'sense',
        Wire.wire >= TransBoard.wire_offset,
        Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)\
    .order_by(
        Wire.sector,
        Wire.superlayer,
        Wire.layer,
        Wire.wire)


    trans_board = np.array(q.all()).T[4].reshape((6,6,6,112))  
    trans_slot = np.array(q.all()).T[5].reshape((6,6,6,112))  
    return trans_board, trans_slot  

def fetchSignalCableArray(session):
    q = session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
           SignalCable.id)\
    .join(Subslot,Doublet,TransBoard, SupplyBoard)\
    .filter(
        SupplyBoard.wire_type == 'sense',
        Wire.wire >= TransBoard.wire_offset,
        Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)\
    .order_by(
        Wire.sector,
        Wire.superlayer,
        Wire.layer,
        Wire.wire)

    signal_cable = np.array(q.all()).T[4]
    return signal_cable.reshape((6,6,6,112))  

def fetchReadoutConnectorArray(session):
    q = session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
           ReadoutConnector.id)\
    .join(Subslot,Doublet,TransBoard, SupplyBoard)\
    .filter(
        SupplyBoard.wire_type == 'sense',
        Wire.wire >= TransBoard.wire_offset,
        Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)\
    .order_by(
        Wire.sector,
        Wire.superlayer,
        Wire.layer,
        Wire.wire)

    readout_connector = np.array(q.all()).T[4]
    return readout_connector.reshape((6,6,6,112))  
    
  

        
if __name__ == '__main__':
    from matplotlib import pyplot
    session = initialize_session()
    dc_fill_tables(session)
    crate = fetchCrateArray(session)
    trans_board, trans_slot = fetchTransBoard(session)
    pyplot.imshow(crate.reshape((72,336)))
    pyplot.show()
  

    
    #print(crate)
    #print(np.sum(crate==1))
    #print(crate.shape)





# In[29]:

#from matplotlib import pyplot


# In[40]:

#sel = crate==1
#sel.shape
#pyplot.imshow(crate[1,2])

