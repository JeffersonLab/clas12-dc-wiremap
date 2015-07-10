import sys
from os import path
import numpy as np

from .dc_tables import (CalibrationDCHVCrate,
    CalibrationDCHVSupplyBoard, CalibrationDCHVSubslot,
    CalibrationDCHVDoublet, CalibrationDCHVDoubletPin,
    CalibrationDCHVDoubletPinMap, CalibrationDCHVTranslationBoard,
    CalibrationDCWire, CalibrationDCSignalTranslationBoard,
    CalibrationDCSignalCable, CalibrationDCSignalReadoutConnector,
    initialize_session)

from . import ccdb_goetz as ccdb
from .cached_property import cached_property

Crate            = CalibrationDCHVCrate
SupplyBoard      = CalibrationDCHVSupplyBoard
Subslot          = CalibrationDCHVSubslot
Doublet          = CalibrationDCHVDoublet
DoubletPin       = CalibrationDCHVDoubletPin
DoubletPinMap    = CalibrationDCHVDoubletPinMap
TransBoard       = CalibrationDCHVTranslationBoard
Wire             = CalibrationDCWire
SignalCable      = CalibrationDCSignalCable
ReadoutConnector = CalibrationDCSignalReadoutConnector

ccdb.rc.connstr = 'mysql://clas12reader@clasdb.jlab.org/clas12'

class DCWires(object):
    _tables = [Crate            ,
               SupplyBoard      ,
               Subslot          ,
               Doublet          ,
               DoubletPin       ,
               DoubletPinMap    ,
               TransBoard       ,
               Wire             ,
               SignalCable      ,
               ReadoutConnector ]

    def __init__(self):
        self.run = 0
        self.variation = 'default'

    @cached_property
    def session(self):
        return initialize_session()

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self,run):
        run = int(run)
        assert run >= 0
        self._run = run

    def clear():
        attrs = '''\
            crate_id
            supply_board_id
        '''.split()
        for attr in attrs:
            try:
                delattr(self,attr)
            except:
                pass

    def fetch_data(self):
        for Table in DCWires._tables:
            name = Table.__tablename__
            print('fetching table:',name)
            data = ccdb.get_table(name,
                run=self.run,
                variation=self.variation)
            for d in data:
                rowdata = {n:np.asscalar(v) for n,v in zip(data.dtype.names, d)}
                row = Table(**rowdata)
                self.session.add(row)
            del data
        self.session.flush()

    @cached_property
    def crate_id(self):

        q = self.session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
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

    @cached_property
    def supply_board_id(self):

        q = self.session.query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
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
        del q
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
