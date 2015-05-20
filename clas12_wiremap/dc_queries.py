from dc_tables import (CalibrationDCHVCrate,
    CalibrationDCHVSupplyBoard, CalibrationDCHVSubslot,
    CalibrationDCHVDoublet, CalibrationDCHVTranslationBoard,
    CalibrationDCWire)

### rename classes for easier reading/writing
Crate = CalibrationDCHVCrate
SupplyBoard = CalibrationDCHVSupplyBoard
Subslot = CalibrationDCHVSubslot
Doublet = CalibrationDCHVDoublet
TransBoard = CalibrationDCHVTranslationBoard
Wire = CalibrationDCWire

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
