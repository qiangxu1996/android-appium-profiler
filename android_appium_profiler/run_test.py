#!/usr/bin/env python

import argparse
import logging
from importlib import import_module

from . import app_test

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('app_script')

    parser.add_argument('-d', '--dummy', action='store_true')
    parser.add_argument('-w', '--warmup', action='store_true')

    parser.add_argument('-c', '--coverage')
    parser.add_argument('-r', '--screen-record')
    parser.add_argument('-l', '--log-file')
    parser.add_argument('-t', '--logcat')
    parser.add_argument('-b', '--battery', action='store_true')

    parser.add_argument('-s', '--server-port', type=int)
    parser.add_argument('-u', '--udid')

    parser.add_argument('-f', '--ftrace', action='store_true')
    parser.add_argument('--ftrace-separate', action='store_true')
    parser.add_argument('--ftrace-file')

    parser.add_argument('--save-state')
    parser.add_argument('--restore-state')

    args = parser.parse_args()

    log_format = '%(created)f %(message)s'
    if args.log_file:
        logging.basicConfig(format=log_format, filename=args.log_file)
    else:
        logging.basicConfig(format=log_format)
    app_test.logger.setLevel(logging.ERROR)

    app = import_module('.apps.' + args.app_script)
    kwargs = dict(a for a in vars(args).items() if a[1] is not None)
    automator = app.App(**kwargs)
    if args.save_state:
        automator.save_state(args.save_state)
    elif args.restore_state:
        automator.restore_state(args.restore_state)
    else:
        automator.run(**kwargs)
