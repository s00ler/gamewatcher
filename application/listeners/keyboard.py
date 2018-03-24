"""Keyboard actions handler."""
from datetime import datetime as dt
from threading import Thread
from pynput import keyboard as kb
import json

from ..action import Action
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
        self.rus_eng = json.loads(open('./rus_eng.json', 'r').read())

    def thread_on_press(self, key):
        job = Thread(target=self.on_press, args=([key]))
        job.start()

    def thread_on_release(self, key):
        job = Thread(target=self.on_release, args=([key]))
        job.start()

    def on_press(self, key):
        """Action on pressing key."""
        if key == kb.Key.f12 and not self.stopped:  # f12 handling
            self.stopped = True
        elif key == kb.Key.f12 and self.stopped:
            self.stopped = False
        elif key == kb.Key.f10:
            Action.input()
        else:
            if not self.stopped:
                key_symbol = str(key)
                if isinstance(key, kb.KeyCode):
                    try:
                        key_code = str(ord(key.char.lower()))
                        key_symbol = key_symbol[1:-1]
                    except Exception:
                        key_code = str(key)
                else:
                    key_code = str(key.name)

                if key_symbol in self.rus_eng:
                    translate = self.rus_eng[key_symbol]
                    key_symbol = translate['eng']
                    key_code = int(translate['code'])

                self.logger.write(KeyboardLog(
                    key_code=key_code,
                    key_symbol=key_symbol,
                    timestamp=dt.utcnow().timestamp(),
                    key_action='press'
                ))

    def on_release(self, key):
        """Action on releasing key."""
        if key not in [kb.Key.f12, kb.Key.f10] and not self.stopped:
            if not self.stopped:
                key_symbol = str(key)
                if isinstance(key, kb.KeyCode):
                    try:
                        key_code = str(ord(key.char.lower()))
                        key_symbol = key_symbol[1:-1]
                    except Exception:
                        key_code = str(key)
                else:
                    key_code = str(key.name)

                if key_symbol in self.rus_eng:
                    translate = self.rus_eng[key_symbol]
                    key_symbol = translate['eng']
                    key_code = int(translate['code'])

                self.logger.write(KeyboardLog(
                    key_code=key_code,
                    key_symbol=key_symbol,
                    timestamp=dt.utcnow().timestamp(),
                    key_action='release'
                ))

    def listen(self):
        """Start listening."""
        with kb.Listener(on_press=self.thread_on_press,
                         on_release=self.thread_on_release) as self.listener:
            self.listener.join()
