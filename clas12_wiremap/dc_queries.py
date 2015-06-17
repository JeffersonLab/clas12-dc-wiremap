import numpy as np

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

def dc_find_connections(session, **kwargs):
    if not hasattr(dc_find_connections, "base_query"):
        dc_find_connections.base_query = session\
            .query(Wire,Subslot,Doublet,TransBoard,SupplyBoard,Crate)\
            .join(Subslot,Doublet,TransBoard,SupplyBoard,Crate)\
            .filter(
                Wire.wire >= TransBoard.wire_offset,
                Wire.wire <  TransBoard.wire_offset + TransBoard.nwires)
    if not hasattr(dc_find_connections, "params"):
        dc_find_connections.params = dict(
            wire_type      = SupplyBoard.wire_type         ,
            sector         = Subslot.sector                ,
            superlayer     = Subslot.superlayer            ,
            layer          = Wire.layer                    ,
            wire           = Wire.wire                     ,
            crate          = Crate.id                      ,
            supply_board   = SupplyBoard.id                ,
            subslot        = Subslot.subslot_id            ,
            channel        = Doublet.channel_id            ,
            distr_box_type = Doublet.distr_box_type        ,
            quad           = Doublet.quad_id               ,
            doublet        = Doublet.doublet_id            ,
            connector      = SupplyBoard.doublet_connector ,
            trans_board    = TransBoard.board_id           ,
            trans_slot     = TransBoard.slot_id            ,)

    q = dc_find_connections.base_query
    p = dc_find_connections.params
    for name in kwargs:
        if kwargs[name] is not None:
            q = q.filter(p[name] == kwargs[name])

    if not hasattr(dc_find_connections, 'all'):
        dc_find_connections.all = True

    if dc_find_connections.all:
        ### Version using Query.all()
        nopts = {}
        fixed = {}
        for name in p:
            if kwargs.get(name,None) is None:
                results = q.from_self(p[name]).distinct().all()
                n = len(results)
                if n == 1:
                    fixed[name] = results[0][0]
                else:
                    nopts[name] = n
    else:
        ### Version using Query.one() with try/except
        nopts = {}
        fixed = {}
        for name in p:
            if kwargs.get(name,None) is None:
                results = q.from_self(p[name]).distinct()
                try:
                    fixed[name], = results.one()
                except:
                    nopts[name] = results.count()

    return fixed,nopts

def dc_wire_status_all(session):
    q = session.query(Wire.status,Doublet.status,SupplyBoard.status,Crate.status)\
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
    wire,doublet,slot,crate = np.array(q.all(), dtype=int).T
    status = wire + 10*doublet + 100*slot + 1000*crate
    status.shape = (6,6,6,112)
    return status

def dc_wire_status(session, **kwargs):
    if not hasattr(dc_wire_status, "base_query"):
        dc_wire_status.base_query = session\
        .query(Wire.sector,Wire.superlayer,Wire.layer,Wire.wire,
               Wire.status,Doublet.status,SupplyBoard.status,
               Crate.status)\
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
    if not hasattr(dc_wire_status, "params"):
        dc_wire_status.params = dict(
            sector         = Subslot.sector                ,
            superlayer     = Subslot.superlayer            ,
            layer          = Wire.layer                    ,
            wire           = Wire.wire                     ,
            crate          = Crate.id                      ,
            supply_board   = SupplyBoard.id                ,
            subslot        = Subslot.subslot_id            ,
            channel        = Doublet.channel_id            ,
            distr_box_type = Doublet.distr_box_type        ,
            quad           = Doublet.quad_id               ,
            doublet        = Doublet.doublet_id            ,
            connector      = SupplyBoard.doublet_connector ,
            trans_board    = TransBoard.board_id           ,
            trans_slot     = TransBoard.slot_id            ,)

    q = dc_wire_status.base_query
    p = dc_wire_status.params
    for name in kwargs:
        if kwargs[name] is not None:
            if name in p:
                q = q.filter(p[name] == kwargs[name])

    stat = np.ones((6,6,6,112), dtype=int)*10000

    res = np.array(q.all(), dtype=int).T
    if res.size:
        sec,slyr,lyr,wr,wstat,dstat,sbstat,ctstat = res
        stat[(sec,slyr,lyr,wr)] = wstat + 10*dstat + 100*sbstat + 1000*ctstat

    return stat
