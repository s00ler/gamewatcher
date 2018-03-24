import sys
from threading import Thread
from configparser import ConfigParser

from utils import ArgParser
from application import Keyboard, Mouse, Logger, Action


if __name__ == '__main__':
    args = ArgParser().parse()
    Action.set(args.a)
    settings = ConfigParser()
    settings.read('settings.ini')

    if args.cs:
        print('Trying to connect to {} database...'.format(args.cs))
        logger = Logger(db_path=settings['DATABASE'][args.cs], batch_time=args.bt)
        print('Connected to specified database.')
    else:
        try:
            print('Establishing remote connection...')
            logger = Logger(db_path=settings['DATABASE']['remote'], batch_time=args.bt)
            print('Connected to remote database.')
        except Exception as remote:
            print('Remote connection failed due to {}.'.format(remote))
            try:
                print('Establishing Local connection...')
                logger = Logger(db_path=settings['DATABASE']['local'], batch_time=args.bt)
                print('Connected to Local database.')
            except Exception as local:
                print('Local connection failed due to {}.'.format(local))
                sys.exit(0)

    mouse_listener = Mouse(logger)
    keyboard_listener = Keyboard(logger)
    threads = [Thread(target=keyboard_listener.listen, daemon=True),
               Thread(target=mouse_listener.listen, daemon=True)]
    try:
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        logger.finalize()
        print('Exitting.')
