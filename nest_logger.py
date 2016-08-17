#!/usr/bin/env python
# nest_logger.py: This program calls the Nest API to log selected data.
# Jacob Hummel

import argparse
import nest
import threading
import logging
from datetime import datetime

#==============================================================================
def get_args():
    programName="nest_logger.py"
    programDescription=" "
    parser = argparse.ArgumentParser(prog=programName,
                                     description=programDescription)
    parser.add_argument("-u","--username",
                        help="Nest Username",
                        required=True)
    parser.add_argument("-p","--password",
                        help="Nest Password",
                        required=True)
    parser.add_argument("-d","--debug",
                        help="Debug Mode: Run once, no threading.",
                        required=False,
                        action="store_true")
    return parser.parse_args()

def datalog(napi, logger, debug=False):
    if(not debug):
        threading.Timer(180,datalog,args=[napi,logger]).start()
    print("Logging Data...")
    log_message = ''
    for structure in napi.structures:
        timestamp = napi._status['structure'][structure.serial]['$timestamp']/1000
        log_message += datetime.fromtimestamp(timestamp).isoformat()
    logger.info(log_message)

def main(args):
    debug = False
    if(args.debug):
        debug = True
        print('Debug Mode Enabled.')
    napi = nest.Nest(username=args.username,password=args.password)
    s = napi.structures[0]
    # create logger
    logger = logging.getLogger('nest_data')
    logger.setLevel(logging.DEBUG)
    # add a file handle
    fh = logging.FileHandler('log.csv')
    # set the formatter for the log.
    frmt = logging.Formatter('%(asctime)s,%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(frmt)
    # add the Handler to the logger
    logger.addHandler(fh)

    datalog(napi, logger, debug)


#==============================================================================
if __name__ == '__main__':
    args = get_args()
    main(args)


