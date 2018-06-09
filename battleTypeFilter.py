#!/usr/bin/env python3

import logging
from wotReplayLib.enums import BattleType
def battleTypeFilter(inputFile, outputFile, battleType):
    """Filters records in inputFile, filtered records are writen to outputFile"""
    for line in inputFile:
        line_segments = line.split(";")
        if len(line_segments) < 5:
            logging.error("Corrupted line %s" % (line))
        elif line_segments[4] == str(battleType.value):
            outputFile.write(line)

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("battleType", help="requested battle type", type=BattleType.fromString, choices=list(BattleType))
    args = parser.parse_args()
    battleTypeFilter(sys.stdin, sys.stdout, args.battleType)
