from sqlalchemy import Column, Float, String, Integer, BigInteger, Numeric
from .base import Base, mac, name


class MouseLog(Base):
    """Implement interface to database table that contains ,ouse logs."""

    __tablename__ = 'gw_mouse_logs'

    id = Column(Integer, primary_key=True)
    author_name = Column(String, default=name)
    author_mac = Column(BigInteger, default=mac)
    action_type = Column(String)
    x = Column(Float)
    y = Column(Float)
    key = Column(String)
    timestamp = Column(Numeric)
    batch = Column(Integer, default=0)
