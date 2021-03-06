"""Mouse actions handler."""
from datetime import datetime as dt

from pynput import mouse

from ..models import MouseLog


class Scroll:
    """Class to handle scroll."""

    def __init__(self):
        """Initialize scroll and set default parameters."""
        self.active = False
        self.coords = (None, None)

    def set(self, x, y):
        """Method to process scroll. Implemented to fix multiple logs on one scrolling.

        param: x, y - coordinates of point where scrolling begin.
        """
        is_changed = False
        if not self.coords == (x, y):
            self.coords = (x, y)
            is_changed = True
        self.active = True
        return is_changed

    def release(self):
        """Reset scroll to defaults."""
        self.__init__()


class Mouse:
    """Class to listen mouse clicks."""

    def __init__(self, logger):
        """Initialize keybord listener.

        param: logger - object that logs listened keys. Must have write method.
        """
        self.logger = logger
        self.listener = None
        self.scroll = Scroll()

    def on_move(self, x, y):
        """Action on moving mouse to point."""
        self.scroll.release()

    def on_click(self, x, y, button, pressed):
        """Action on clicking mouse at the point."""
        self.scroll.release()
        click_type = str(button).split('.')[-1]
        self.logger.write(MouseLog(x=x, y=y, key=click_type,
                                   timestamp=dt.utcnow().timestamp()))

    def on_scroll(self, x, y, dx, dy):
        """Action on scrolling mouse at the point."""
        if self.scroll.set(x, y):
            self.logger.write(MouseLog(x=x, y=y, key='scroll',
                                       timestamp=dt.utcnow().timestamp()))

    def listen(self):
        """Start listening."""
        with mouse.Listener(on_move=self.on_move,
                            on_click=self.on_click,
                            on_scroll=self.on_scroll) as self.listener:
            self.listener.join()
