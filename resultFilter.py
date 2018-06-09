#!/usr/bin/env python3

import logging
from wotReplayLib.enums import BattleResult
def resultFilter(inputFile, outputFile, result):
    """Filters records in inputFile, filtered records are writen to outputFile"""
    for line in inputFile:
        line_segments = line.split(";")
        if len(line_segments) < 10:
            logging.error("Corrupted line %s" % (line))
        elif line_segments[9] == str(result.value):
            outputFile.write(line)

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("battleResult", help="requested battle result", type=BattleResult.fromString, choices=list(BattleResult)
    args = parser.parse_args()
    resultFilter(sys.stdin, sys.stdout, args.battleResult)
