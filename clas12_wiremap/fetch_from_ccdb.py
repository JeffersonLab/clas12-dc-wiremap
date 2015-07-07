import numpy as np

from clas12_wiremap import db

from .dc_tables import (CalibrationDCHVCrate,
    CalibrationDCHVSupplyBoard, CalibrationDCHVSubslot,
    CalibrationDCHVDoublet, CalibrationDCHVDoubletPin,
    CalibrationDCHVDoubletPinMap, CalibrationDCHVTranslationBoard,
    CalibrationDCWire, CalibrationDCSignalTranslationBoard,
    CalibrationDCSignalCable, CalibrationDCSignalReadoutConnector)

### rename classes for easier reading/writing
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

def dc_fetch_tables(session):
    def fetch(table):
        return ccdb.get_table('/calibration/drift_chamber/'+table)

    rows = Crate.from_array(fetch('high_voltage/crate'))
    session.add_all(rows)

if __name__ == '__main__':
    from ccdb import *
    session = initialize_session()

    dc_fetch_tables(session)

    q = session.query(Crate)
    for r in q:
        print(r)
