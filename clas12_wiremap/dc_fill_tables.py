import itertools as it

from .dc_tables import (CalibrationDCHVCrate,
    CalibrationDCHVSupplyBoard, CalibrationDCHVSubslot,
    CalibrationDCHVDoublet, CalibrationDCHVDoubletPin,
    CalibrationDCHVDoubletPinMap, CalibrationDCHVTranslationBoard,
    CalibrationDCWire, CalibrationDCSignalTranslationBoard,
    CalibrationDCSignalCable, CalibrationDCSignalReadoutConnector)

def dc_fill_tables(session):

    # utility functions
    def repeat(lst, n):
        return list(it.chain(*it.repeat(lst,n)))

    def repeat_elements(lst,n=2):
        return list(it.chain(*([i]*n for i in lst)))

    # DC HV Crate
    crates = range(4)

    for crate_id in crates:
        row = CalibrationDCHVCrate(id=crate_id,status=0)
        session.add(row)

    # DC HV Supply Board
    def slots(crate):
        if crate_id < 2:
            return range(5)
        else:
            return range(10)

    def wire_type(slot):
        if (slot % 5) < 2:
            return 'sense'
        elif (slot % 5) < 4:
            return 'field'
        else:
            return 'guard'

    def doublet_connector(wtype):
        if wtype in ['sense','guard']:
            return 1
        else:
            return 0

    supply_board_id = 0
    for crate_id in crates:
        for slot_id in slots(crate_id):

            wtype = wire_type(slot_id)
            conn = doublet_connector(wtype)

            row = CalibrationDCHVSupplyBoard(
                id                = supply_board_id,
                crate_id          = crate_id,
                slot_id           = slot_id,
                wire_type         = wtype,
                doublet_connector = conn,
                status            = 0)
            session.add(row)

            supply_board_id += 1

    # DC HV Supply Board Subslots
    def subslots(slot):
        if (slot % 5) < 4:
            return range(3)
        else:
            return range(6)

    def sector(crate,slot,subslot):

        if (crate % 2) > 0:
            sec = repeat(repeat_elements((4,3,2)),3)
        else:
            sec = repeat(repeat_elements((5,0,1)),3)

        i = sum(len(subslots(s)) for s in range(slot))
        i += subslot
        return sec[i % 18]

    def superlayer(crate,slot,subslot):

        if crate < 2:
            slyr = repeat((0,1),9)
        elif slot < 5:
            slyr = repeat((2,3),9)
        else:
            slyr = repeat((4,5),9)

        i = sum(len(subslots(s)) for s in range(slot))
        i += subslot
        return slyr[i % 18]

    supply_board_id = 0
    for crate_id in crates:
        for slot_id in slots(crate_id):
            for subslot_id in subslots(slot_id):

                sec = sector(crate_id,slot_id,subslot_id)
                slyr = superlayer(crate_id,slot_id,subslot_id)

                row = CalibrationDCHVSubslot(
                    supply_board_id = supply_board_id,
                    subslot_id = subslot_id,
                    sector = sec,
                    superlayer = slyr)
                session.add(row)

            supply_board_id += 1

    # DC HV Doublet Connectors and Pins
    def channels(wire_type):
        if wire_type in ['sense','field']:
            return list(range(4)) + repeat_elements(range(4,9))
        else:
            return [0]*6 + [1]*6

    box_types = ['forward']*6 + ['backward']*6

    quads = repeat(repeat_elements(range(3)),2)

    doublets = repeat(range(2),6)
    pins = range(9)

    trans_boards = repeat_elements(range(5))+list(range(5,7))

    trans_slots = repeat(range(2),5)+[0]*2

    supply_board_id = 0
    doublet_id = 0
    for crate_id in crates:
        for slot_id in slots(crate_id):
            wtype = wire_type(slot_id)
            for subslot_id in subslots(slot_id):
                for ch,btype,q,d,tb,ts in zip(channels(wtype),box_types,quads,doublets,trans_boards,trans_slots):
                    row = CalibrationDCHVDoublet(
                        id = doublet_id,
                        supply_board_id = supply_board_id,
                        subslot_id = subslot_id,
                        channel_id = ch,
                        distr_box_type = btype,
                        quad_id = q,
                        doublet_id = d,
                        trans_board_id = tb,
                        trans_slot_id = ts,
                        status = 0)
                    session.add(row)

                    for pin_id in pins:
                        row = CalibrationDCHVDoubletPin(
                            doublet_id=doublet_id,
                            pin_id=pin_id,
                            status=0)
                        session.add(row)

                    doublet_id += 1

            supply_board_id += 1


    # DC HV Doublet Pin Map
    doublet_halves = range(2)
    for doublet_id in doublet_halves:
        for pin_id in pins:
            if doublet_id < 1:
                if pin_id < 7:
                    wtype = 'field'
                    layers = [2*pin_id,2*pin_id+1]
                else:
                    continue
            else:
                if pin_id < 2:
                    wtype = 'guard'
                    layers = [pin_id]
                elif pin_id < 8:
                    wtype = 'sense'
                    layers = [pin_id - 2]
                else:
                    continue
            for layer_id in layers:
                row = CalibrationDCHVDoubletPinMap(
                    doublet_id = doublet_id,
                    pin_id = pin_id,
                    wire_type = wtype,
                    layer = layer_id)
                session.add(row)

    # DC HV Translation Boards
    translation_boards = range(7)

    def translation_slots(board):
        if board < 5:
            return range(2)
        else:
            return range(1)

    def wire_offset(board,slot):
        if board < 5:
            i = board*2 + slot
        else:
            i = 5*2 + (board - 5) + slot
        woffs = list(range(0,80,8))+list(range(80,112,16))
        return woffs[i]

    def nwires(board):
        if board < 5:
            return 8
        else:
            return 16

    for board_id in translation_boards:
        for slot_id in translation_slots(board_id):
            row = CalibrationDCHVTranslationBoard(
                board_id = board_id,
                slot_id = slot_id,
                wire_offset = wire_offset(board_id,slot_id),
                nwires = nwires(board_id))
            session.add(row)

    # DC Sense Wires
    sectors = range(6)
    superlayers = range(6)
    layers = range(6)
    wires = range(112)

    for sector_id in sectors:
        for superlayer_id in superlayers:
            for layer_id in layers:
                for wire_id in wires:
                    row = CalibrationDCWire(
                        sector = sector_id,
                        superlayer = superlayer_id,
                        layer = layer_id,
                        wire = wire_id,
                        status = 0)
                    session.add(row)

    # DC Signal Translation Boards
    translation_boards = range(7)
    nwires = 16
    wire_offsets = list(range(0,112,nwires))

    for board_id in translation_boards:
        row = CalibrationDCSignalTranslationBoard(
            id = board_id,
            wire_offset = wire_offsets[board_id],
            nwires = 16)
        session.add(row)

    # DC Signal Cables

    def connector_id(layer_id):
        return layer_id

    cable_id = 0
    for sector in sectors:
        for superlayer in superlayers:
            for layer in layers:
                for board_id in translation_boards:
                    row = CalibrationDCSignalCable(
                        id=cable_id,
                        sector=sector,
                        superlayer=superlayer,
                        layer=layer,
                        board_id=board_id,
                        connector_id=connector_id(layer),
                        time_delay=0,
                        fuse_status=0,
                        cable_status=0)
                    session.add(row)
                    cable_id += 1

    session.flush()
