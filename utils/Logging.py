from __future__ import print_function

import os

from datetime import datetime


def log(message, debug=True):
    import inspect
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    log_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    if debug:
        print("%s - %s:%s() - %s" %
              (log_time,
               os.path.splitext(os.path.basename(func.co_filename))[0],
               func.co_name,
               message))
