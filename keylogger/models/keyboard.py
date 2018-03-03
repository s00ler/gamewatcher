from sqlalchemy import Column, String, Integer, Numeric, BigInteger
from .base import Base, mac, name


class KeyboardLog(Base):
    """Implement interface to database table that contains keyboard logs."""

    __tablename__ = 'gw_keyboard_logs'

    id = Column(Integer, primary_key=True)
    author_name = Column(String, default=name)
    author_mac = Column(BigInteger, default=mac)
    action_type = Column(String)
    key_action = Column(String)
    key_code = Column(String)
    key_symbol = Column(String)
    timestamp = Column(Numeric)
    batch = Column(Integer, default=0)
