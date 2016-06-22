from datetime import datetime
import os

def log(message):
    import inspect
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    log_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print("%s - %s:%s()  %s" % (
        log_time,
        os.path.splitext(os.path.basename(func.co_filename))[0],
        func.co_name,
        message))