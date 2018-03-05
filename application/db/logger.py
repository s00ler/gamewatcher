"""Logging module."""
from copy import copy
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker

from ..models import Base, KeyboardLog
from ..action import Action

BATCH_TIME = 120


class Logger:
    """Class contains methods to connect and write to database."""

    def __init__(self, db_path=None, batch_time=None):
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
            self._batch_num = self.session.query(
                func.max(KeyboardLog.batch)).scalar() + 1 or 0
            self._batch_time = int(
                batch_time) if batch_time is not None else BATCH_TIME
            self._uploading = False


    def _upload(self, *to_load):
        self._uploading = True
        self._batch_num += 1
        self.session.add_all(to_load)
        self.session.commit()
        self._uploading = False
        print('Batch uploaded.')

    def finalize(self):
        """Call after interrupt event."""
        if not self._uploading:
            self.session.add_all(self.to_load)
            self.to_load = []
            self.session.commit()

    def write(self, data):
        """Create database session and writes to database.

        param: data - data to write into database.
        """
        if not self.to_load:
            self.start_timestamp = data.timestamp
        if data.timestamp - self.start_timestamp > self._batch_time and not self._uploading:
            self.start_timestamp = data.timestamp
            uploader = Thread(target=self._upload, args=copy(self.to_load))
            uploader.start()
            self.to_load = []

        data.batch = self._batch_num
        data.action_type = Action.get()
        self.to_load.append(data)
