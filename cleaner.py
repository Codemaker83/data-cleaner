#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path",
                    help="Path of backup dir", required=True)
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
limit = int(args.limit)


def get_date(filename):
    date_str = filename.split(".")[0]
    str_list = date_str.split("-")
    str_list = str_list[len(str_list) - 1].split("_")
    date_str = str_list[len(str_list) - 2]
    year = int(date_str[0:4])
    month = int(date_str[4:6])
    day = int(date_str[6:])
    try:
        file_date = datetime.date(year, month, day)
    except Exception as e:
        logger.error(e)
        file_date = datetime.date.today()
    return file_date


def remove(path, limit):
    today = datetime.date.today()
    logger.debug("%s", today)
    for dfile in os.listdir(path):
        filename = os.path.abspath(os.path.join(path, dfile))
        dt = today - get_date(filename)
        logger.debug("%s file found: %s days", dfile, dt.days)
        if dt.days > limit:
            logger.debug("%s file above limit", dfile)
            logger.info("Removing %s", dfile)
            os.remove(filename)
    return path

if __name__ == '__main__':
    logger.info("Executing cleaner. Date: %s", datetime.date.today())
    remove(path, limit)
    logger.info("Backup dir cleaned")
