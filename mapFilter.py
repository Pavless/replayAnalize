#!/usr/bin/env python3

import logging

def mapFilter(inputFile, outputFile, m):
    """Filters records in inputFile, filtered records are writen to outputFile"""
    for line in inputFile:
        line_segments = line.split(";")
        if len(line_segments) < 4:
            logging.error("Corrupted line %s" % (line))
        elif line_segments[3] == m:
            outputFile.write(line)

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("map", help="requested map")
    args = parser.parse_args()
    mapFilter(sys.stdin, sys.stdout, args.map)
