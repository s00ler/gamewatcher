"""Keyboard actions handler."""
from datetime import datetime as dt
from threading import Thread
from pynput import keyboard as kb

from ..action import _type, input_action_type
from ..models import KeyboardLog


class Keyboard:
    """Class to listen keys pressed."""

    def __init__(self, logger):
        """Initialize keybord listener.

        param: logger - object that logs listened keys. Must have write method.
        """
        self.logger = logger
        self.listener = None
        self.stopped = False

    def on_press(self, key):
        job = Thread(target=self._on_press, args=([key]))
        job.start()

    def on_release(self, key):
        job = Thread(target=self._on_release, args=([key]))
        job.start()

    def _on_press(self, key):
        """Action on pressing key."""
        if key == kb.Key.f12 and not self.stopped:  # f12 handling
            self.stopped = True
        elif key == kb.Key.f12 and self.stopped:
            self.stopped = False
        elif key == kb.Key.f10:
            input_action_type()
        else:
            if not self.stopped:
                if isinstance(key, kb.KeyCode):
                    try:
                        key_code = str(ord(key.char.lower()))
                    except Exception:
                        key_code = str(key)
                else:
                    key_code = str(key.name)
                self.logger.write(KeyboardLog(
                    key_code=key_code,
                    key_symbol=str(key),
                    action_type=_type,
                    timestamp=dt.utcnow().timestamp(),
                    key_action='press'
                ))

    def _on_release(self, key):
        """Action on releasing key."""
        if key not in [kb.Key.f12, kb.Key.f10] and not self.stopped:
            if not self.stopped:
                if isinstance(key, kb.KeyCode):
                    try:
                        key_code = str(ord(key.char.lower()))
                    except Exception:
                        key_code = str(key)
                else:
                    key_code = str(key.name)
                self.logger.write(KeyboardLog(
                    key_code=key_code,
                    key_symbol=str(key),
                    action_type=_type,
                    timestamp=dt.utcnow().timestamp(),
                    key_action='release'
                ))

    def listen(self):
        """Start listening."""
        with kb.Listener(on_press=self.on_press,
                         on_release=self.on_release) as self.listener:
            self.listener.join()
