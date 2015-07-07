import re

from sqlalchemy import Column, Integer, Float, Enum
from sqlalchemy import ForeignKey, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

def initialize_session(engine_init = 'sqlite:///:memory:'):
    engine = create_engine(engine_init)
    Base.metadata.bind = engine
    session = sessionmaker(bind=engine)()
    Base.metadata.create_all()
    return session

class CalibrationDCHVCrate(Base):
    __tablename__ = '/calibration/dc/hv_crate'
    id     = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    supply_boards = relationship('CalibrationDCHVSupplyBoard', backref='crate')

    @staticmethod
    def from_array(arr):
        ret = []
        for a in arr:
            ret.append(CalibrationDCHVCrate(id=a[0],status=a[1]))
        return ret

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
    pin_id     = Column(Integer, primary_key=True)
    status     = Column(Integer, nullable=False)
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


