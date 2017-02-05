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
    else:
        print('Logging data...')
    for structure in napi.structures:
        for device in structure.devices:
            log_message = ''
            log_message += "{}".format(device.serial)
            log_message += ",{}".format(int(structure.away))
            log_message += ",{:0.1f}".format(device.temperature)
            log_message += ",{:0.1f}".format(device.humidity)
            log_message += ",{}".format(device.mode)
            if device.mode == 'range':
                log_message += ",{:0.1f},{:0.1f}".format(*device.target)
            elif device.mode == 'cool':
                log_message += ",{:0.1f},".format(device.target)
            elif device.mode == 'heat':
                log_message += ",,{:0.1f}".format(device.target)
            else:
                log_message += ",,"
            log_message += ",{}".format(int(device.leaf))
            log_message += ",{:0.1f}".format(device.leaf_threshold_cool)
            log_message += ",{:0.1f}".format(device.leaf_threshold_heat)
            log_message += ",{}".format(int(device.fan))
            log_message += ",{}".format(int(device.hvac_ac_state))
            log_message += ",{}".format(int(device.hvac_heater_state))
            log_message += ",{}".format(structure.weather.current.condition)
            log_message += ",{:0.1f}".format(structure.weather.current.temperature)
            log_message += ",{:0.1f}".format(structure.weather.current.humidity)
            log_message += ",{}".format(structure.weather.current.wind.direction)
            log_message += ",{:0.1f}".format(structure.weather.current.wind.azimuth)
            #log_message += ",{:0.1f}".format(structure.weather.current.wind.kph)
            logger.info(log_message)
    if debug:
        print(log_message)

def main(args):
    debug = False
    if(args.debug):
        debug = True
        print('Debug Mode Enabled.')
    else:
        print('Pinging nest every 3 minutes...')

    napi = nest.Nest(username=args.username,password=args.password)#,cache_ttl=0)
    s = napi.structures[0]
    # create logger
    logger = logging.getLogger('nest_data')
    logger.setLevel(logging.DEBUG)
    # add a file handle
    fh = logging.FileHandler('nest_data_log.csv')
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


