#!/usr/bin/env python3

import logging

def playerFilter(inputFile, outputFile, player):
    """Filters records in inputFile, filtered records are writen to outputFile"""
    for line in inputFile:
        line_segments = line.split(";")
        if len(line_segments) < 6:
            logging.error("Corrupted line %s" % (line))
        elif line_segments[5] == player:
            outputFile.write(line)

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("playerName", help="requested player name")
    args = parser.parse_args()
    playerFilter(sys.stdin, sys.stdout, args.playerName)
