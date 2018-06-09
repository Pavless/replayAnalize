#!/usr/bin/env python3

import logging

def blockFilter(inputFile, outputFile, count):
    """Filters records in inputFile, filtered records are writen to outputFile"""
    for line in inputFile:
        line_segments = line.split(";")
        if len(line_segments) < 2:
            logging.error("Corrupted line %s" % (line))
        elif line_segments[1] == str(count):
            outputFile.write(line)

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("blockCount", help="requested number of blocks", type=int, choices=[1,2,3])
    args = parser.parse_args()
    blockFilter(sys.stdin, sys.stdout, args.blockCount)
