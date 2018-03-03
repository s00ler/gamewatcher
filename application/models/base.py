from sqlalchemy.ext.declarative import declarative_base
from uuid import getnode as get_mac
import platform


Base = declarative_base()
mac = get_mac()
name = platform.node()
