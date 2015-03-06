#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path",
                    help="Path of backup dir, actual dir by default",
                    required=True)
parser.add_argument("-L", "--limit",
                    help="Maximum days allowed (15 by default)",
                    default=15)
parser.add_argument("--log-level", help="Level of logger. INFO as default",
                    default="info")
parser.add_argument("--logfile", help="File where log will be saved",
                    default=None)

args = parser.parse_args()
level = getattr(logging, args.log_level.upper(), None)

logging.basicConfig(level=level,
                    filename=args.logfile,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('cleaner')

path = args.path
limit = args.limit


def get_date(filename):
    t = os.path.getmtime(filename)
    date_list = str(datetime.datetime.fromtimestamp(t)).split()[0].split("-")
    year = int(date_list[0])
    month = int(date_list[1])
    day = int(date_list[2])
    return datetime.date(year, month, day)


def remove(path, limit):
    today = datetime.date.today()
    for dfile in os.listdir(path):
        logger.debug("%s file found", dfile)
        filename = os.path.abspath(os.path.join(path, dfile))
        dt = today - get_date(filename)
        if dt.days > limit:
            logger.debug("%s file above limit")
            logger.info("Removing %s", dfile)
            os.remove(filename)
    return path

if __name__ == '__main__':
    logger.info("Executing cleaner")
    remove(path, limit)
    logger.info("Backup dir cleaned")
