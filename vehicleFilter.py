#!/usr/bin/env python3

import logging

def vehicleFilter(inputFile, outputFile, vehicle):
    """Filters records in inputFile, filtered records are writen to outputFile"""
    for line in inputFile:
        line_segments = line.split(";")
        if len(line_segments) < 8:
            logging.error("Corrupted line %s" % (line))
        elif line_segments[7] == vehicle:
            outputFile.write(line)

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("vehicle", help="requested player name")
    args = parser.parse_args()
    vehicleFilter(sys.stdin, sys.stdout, args.vehicle)
