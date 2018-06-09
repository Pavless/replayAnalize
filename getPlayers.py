#!/usr/bin/env python3

import logging

def getPlayers(inputFile, outputFile):
    """Gets all unique records in inputFile, filtered records are writen to outputFile"""
    players = set()
    for line in inputFile:
        line_segments = line.split(";")
        if len(line_segments) < 6:
            logging.error("Corrupted line %s" % (line))
        players.add(line_segments[5])
    
    for player in players:
        outputFile.write(player + "\n")

if __name__ == "__main__":
    import sys
    getPlayers(sys.stdin, sys.stdout)
