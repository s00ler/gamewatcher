from sqlalchemy import Column, Float, String, Integer, BigInteger, Numeric
from .base import Base, mac, name, ToDictMixin


class MouseLog(Base, ToDictMixin):
    """Implement interface to database table that contains ,ouse logs."""

    __tablename__ = 'gw_mouse_logs'

    id = Column(Integer, primary_key=True)
    author_name = Column(String, default=name)
    author_mac = Column(BigInteger, default=mac)
    action_type = Column(String, default=None)
    x = Column(Float)
    y = Column(Float)
    key = Column(String)
    timestamp = Column(Numeric)
    batch = Column(Integer, default=0)
