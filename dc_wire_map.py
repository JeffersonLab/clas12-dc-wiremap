import re
import itertools as it

from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy import ForeignKey, ForeignKeyConstraint, UniqueConstraint, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, join
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///:memory:')
Base.metadata.bind = engine
session = sessionmaker(bind=engine)()

class CalibrationDCHVCrate(Base):
    __tablename__ = '/calibration/dc/hv_crate'
    id     = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    supply_boards = relationship('CalibrationDCHVSupplyBoard', backref='crate')
    def __str__(self):
        fmt = '[{id}]({status})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = 'CalibrationDCHVCrate(id={id},status={status})'
        return fmt.format(**vars(self))

class CalibrationDCHVSupplyBoard(Base):
    __tablename__ = '/calibration/dc/hv_supply_board'
    id        = Column(Integer, primary_key=True)
    crate_id  = Column(Integer, ForeignKey('/calibration/dc/hv_crate.id'))
    slot_id   = Column(Integer, nullable=False)
    wire_type = Column(Enum('sense','field','guard'))
    doublet_connector = Column(Integer, nullable=False)
    status    = Column(Integer, nullable=False)
    subslots = relationship('CalibrationDCHVSubslot', backref='supply_board')
    __table_args__ = (
        UniqueConstraint(
            'crate_id',
            'slot_id'),)
    def __str__(self):
        fmt = '[{id}/{crate_id},{slot_id}]({wire_type},{doublet_connector},{status})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCHVSupplyBoard(
                id={id},
                crate_id={crate_id},
                slot_id={slot_id},
                wire_type={wire_type},
                doublet_connector={doublet_connector},
                status={status})''')
        return fmt.format(**vars(self))

class CalibrationDCHVSubslot(Base):
    __tablename__ = '/calibration/dc/hv_subslot'
    supply_board_id = Column(Integer, ForeignKey('/calibration/dc/hv_supply_board.id'), primary_key=True)
    subslot_id      = Column(Integer, primary_key=True)
    sector          = Column(Integer, nullable=False)
    superlayer      = Column(Integer, nullable=False)
    doublets = relationship('CalibrationDCHVDoublet', backref='subslot')
    def __str__(self):
        fmt = '[{supply_board_id},{subslot_id}]({sector},{superlayer})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCHVSubslot(
                supply_board_id={supply_board_id},
                subslot_id={subslot_id},
                sector={sector},
                superlayer={superlayer})''')
        return fmt.format(**vars(self))

class CalibrationDCHVDoublet(Base):
    __tablename__ = '/calibration/dc/hv_doublet'
    id                = Column(Integer, primary_key=True)
    supply_board_id   = Column(Integer, nullable=False)
    subslot_id        = Column(Integer, nullable=False)
    channel_id        = Column(Integer, nullable=False)
    distr_box_type    = Column(Enum('forward','backward'), nullable=False)
    quad_id           = Column(Integer, nullable=False)
    doublet_id        = Column(Integer, nullable=False)
    trans_board_id    = Column(Integer, nullable=False)
    trans_slot_id     = Column(Integer, nullable=False)
    status            = Column(Integer, nullable=False)
    trans_board = relationship('CalibrationDCHVTranslationBoard', backref='doublets')
    pins = relationship('CalibrationDCHVDoubletPin', backref='doublet')
    __table_args__ = (
        ForeignKeyConstraint(
            ['supply_board_id','subslot_id'],
            ['/calibration/dc/hv_subslot.supply_board_id',
             '/calibration/dc/hv_subslot.subslot_id']),
        ForeignKeyConstraint(
            ['trans_board_id','trans_slot_id'],
            ['/calibration/dc/hv_translation_board.board_id',
             '/calibration/dc/hv_translation_board.slot_id']),
        UniqueConstraint(
            'supply_board_id',
            'subslot_id',
            'distr_box_type',
            'quad_id',
            'doublet_id'),
        UniqueConstraint(
            'supply_board_id',
            'subslot_id',
            'trans_board_id',
            'trans_slot_id'),)
    def __str__(self):
        fmt = '[{id}]'\
            + '({supply_board_id},{subslot_id},{channel_id},'\
            + '{distr_box_type},{quad_id},{doublet_id},'\
            + '{status})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCHVDoublet(
                id={id},
                supply_board_id={supply_board_id},
                subslot_id={subslot_id},
                channel_id={channel_id},
                distr_box_type={distr_box_type},
                quad_id={quad_id},
                doublet_id={doublet_id},
                status={status})''')
        return fmt.format(**vars(self))

class CalibrationDCHVDoubletPin(Base):
    __tablename__ = '/calibration/dc/hv_doublet_pin'
    doublet_id = Column(Integer, ForeignKey('/calibration/dc/hv_doublet.id'), primary_key=True)
    pin_id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    def __str__(self):
        fmt = '[{doublet_id},{pin_id}]({status})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCHVDoubletPin(
                doublet_id={doublet_id},
                pin_id={pin_id},
                status={status})''')
        return fmt.format(**vars(self))

class CalibrationDCHVDoubletPinMap(Base):
    __tablename__ = '/calibration/dc/hv_doublet_pin_map'
    doublet_id = Column(Integer, ForeignKey('/calibration/dc/hv_doublet.doublet_id'), primary_key=True)
    pin_id     = Column(Integer, ForeignKey('/calibration/dc/hv_doublet_pin.pin_id'), primary_key=True)
    wire_type  = Column(Enum('sense','field','guard'),
                        ForeignKey('/calibration/dc/hv_supply_board.wire_type'), primary_key=True)
    layer      = Column(Integer, ForeignKey('/calibration/dc/wire.layer'), primary_key=True)
    def __str__(self):
        fmt = '[{doublet_id},{pin_id}/{wire_type},{layer}]'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCHVDoubletPinMap(
                doublet_id={doublet_id},
                pin_id={pin_id},
                wire_type={wire_type},
                layer={layer})''')
        return fmt.format(**vars(self))

class CalibrationDCHVTranslationBoard(Base):
    __tablename__ = '/calibration/dc/hv_translation_board'
    board_id    = Column(Integer, primary_key=True)
    slot_id     = Column(Integer, primary_key=True)
    wire_offset = Column(Integer, nullable=False)
    nwires      = Column(Integer, nullable=False)
    def __str__(self):
        fmt = '[{board_id},{slot_id}]({wire_offset},{nwires})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCHVTranslationBoard(
                board_id={board_id},
                slot_id={slot_id},
                wire_offset={wire_offset},
                nwires={nwires})''')
        return fmt.format(**vars(self))

class CalibrationDCWire(Base):
    __tablename__ = '/calibration/dc/wire'
    sector     = Column(Integer, primary_key=True)
    superlayer = Column(Integer, primary_key=True)
    layer      = Column(Integer, primary_key=True)
    wire       = Column(Integer, primary_key=True)
    status     = Column(Integer, nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(
            ['sector','superlayer'],
            ['/calibration/dc/hv_subslot.sector',
             '/calibration/dc/hv_subslot.superlayer']),)
    def __str__(self):
        fmt = '[{sector},{superlayer},{layer},{wire}]({status})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCWire(
                sector={sector},
                superlayer={superlayer},
                layer={layer},
                wire={wire},
                status={status})''')
        return fmt.format(**vars(self))

class CalibrationDCSignalTranslationBoard(Base):
    __tablename__ = '/calibration/dc/signal_translation_board'
    id          = Column(Integer, primary_key=True)
    wire_offset = Column(Integer, nullable=False)
    nwires      = Column(Integer, nullable=False)
    def __str__(self):
        fmt = '[{id}]({wire_offset},{nwires})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCSignalTranslationBoard(
                id={id},
                wire_offset={wire_offset},
                nwires={nwires})''')
        return fmt.format(**vars(self))

class CalibrationDCSignalCable(Base):
    __tablename__ = '/calibration/dc/signal_cable'
    id           = Column(Integer, primary_key=True)
    sector       = Column(Integer, nullable=False)
    superlayer   = Column(Integer, nullable=False)
    layer        = Column(Integer, nullable=False)
    board_id     = Column(Integer, ForeignKey('/calibration/dc/signal_translation_board.id'), nullable=False)
    connector_id = Column(Integer, nullable=False)
    time_delay   = Column(Float,   nullable=False)
    fuse_status  = Column(Integer, nullable=False)
    cable_status = Column(Integer, nullable=False)

    readout_connector = relationship('CalibrationDCSignalReadoutConnector', uselist=False, backref='cable')

    __table_args__ = (
        ForeignKeyConstraint(
            ['sector','superlayer','layer'],
            ['/calibration/dc/wire.sector',
             '/calibration/dc/wire.superlayer',
             '/calibration/dc/wire.layer']),
        UniqueConstraint(
            'sector',
            'superlayer',
            'board_id',
            'connector_id'),)
    def __str__(self):
        fmt = '[{id}/'\
            + '{sector},{superlayer},{layer}/'\
            + '{board_id},{connector_id}]'\
            + '({time_delay},{fuse_status},{cable_status})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCSignalCable(
                id={id},
                sector={sector},
                superlayer={superlayer},
                board_id={board_id},
                connector_id={connector_id},
                time_delay={time_delay},
                fuse_status={fuse_status},
                cable_status={cable_status})''')
        return fmt.format(**vars(self))

class CalibrationDCSignalReadoutConnector(Base):
    __tablename__ = '/calibration/dc/signal_readout_connector'
    id           = Column(Integer, primary_key=True)
    cable_id     = Column(Integer, ForeignKey('/calibration/dc/signal_cable.id'))
    crate_id     = Column(Integer, nullable=False)
    slot_id      = Column(Integer, nullable=False)
    connector_id = Column(Integer, nullable=False)
    status       = Column(Integer, nullable=False)
    __table_args__ = (
        UniqueConstraint(
            'crate_id',
            'slot_id',
            'connector_id'),)
    def __str__(self):
        fmt = '[{id}/{cable_id}/{crate_id},{slot_id},{connector_id}]({status})'
        return fmt.format(**vars(self))
    def __repr__(self):
        fmt = re.sub(r'\s+','','''\
            CalibrationDCSignalReadoutConnector(
                id={id}
                cable_id={cable_id},
                crate_id={crate_id},
                slot_id={slot_id},
                connector_id={connector_id},
                status={status})''')
        return fmt.format(**vars(self))

Base.metadata.create_all()
















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
