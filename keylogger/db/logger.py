"""Logging module."""
from threading import Thread
from copy import copy

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker

from ..models import Base, KeyboardLog

BATCH_TIME = 120


class Logger:
    """Class contains methods to connect and write to database."""

    def __init__(self, db_path=None):
        """Initialize connection to database.

        param: db_path - database connection string.
        """
        if db_path is not None:
            engine = create_engine(db_path, echo=False)
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            Session.configure(bind=engine)
            self.session = Session()
            self.to_load = []
            self._batch_num = self.session.query(func.max(KeyboardLog.batch)) or 0

    def _upload(self, to_load):
        self.session.add_all(to_load)
        self.session.commit()

    def finalize(self):
        self.session.add_all(self.to_load)
        self.to_load = []
        self.session.commit()

    def write(self, data):
        """Create database session and writes to database.

        param: data - data to write into database.
        """
        if not self.to_load:
            self.start_timestamp = data.timestamp
        if data.timestamp - self.start_timestamp > BATCH_TIME:
            self._batch_num += 1
            self.start_timestamp = data.timestamp
            thread = Thread(target=self._upload, args=copy(self.to_load))
            thread.start()
            self.to_load = []
        data.batch = self._batch_num
        self.to_load.append(data)
