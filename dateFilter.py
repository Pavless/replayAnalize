#!/usr/bin/env python3

import logging
from datetime import datetime
from datetime import date
def dateFilter(inputFile, outputFile, d):
    """Filters records in inputFile, filtered records are writen to outputFile"""
    for line in inputFile:
        line_segments = line.split(";")
        if len(line_segments) < 3:
            logging.error("Corrupted line %s" % (line))
        else:
            try:
                line_d = datetime.strptime(line_segments[2], "%d.%m.%Y %H:%M:%S")
                if line_d.date() == d:
                    outputFile.write(line)
            except ValueError:
                logging.error("Unable to parse datetime %s" % (line_segment[1]))

from argparse import ArgumentTypeError
def validate_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: %s" % (s)
        raise ArgumentTypeError(msg)

if __name__ == "__main__":
    import sys
    logging.basicConfig(filename="dateFilter.log")

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("date", help="requested date, format: YYYY-MM-DD", type=validate_date)
    args = parser.parse_args()
    dateFilter(sys.stdin, sys.stdout, args.date)
