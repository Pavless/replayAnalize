#!/usr/bin/env python3

from wotReplayLib.blocks import extractBlocks
from wotReplayLib.rawExtraction import extractRaw

import logging
import json
import os

def extractRawFromDir(directory, saveJson=False):
    """Runs raw extraction on each .wotreplay file in the directory
    
    Returns: list of lines"""
    # validate directory
    if not os.path.isdir(directory):
        logging.error("%s is not a valid directory" % (directory))
        raise ValueError("%s is not a valid directory" % (directory))

    logging.info("Starting directory raw extraction from %s" % (directory))
    rawReplay = []
    rawPlayer = []
    for f in [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".wotreplay")]:
        logging.info("Starting block extraction from %s" % (f))
        with open(f, "rb") as openedFile:
            blocks = extractBlocks(openedFile)
        logging.info("Finished block extraction from %s" % (f))
        logging.info("Starting raw extraction from %s blocks" % (f))

        # save Json dump
        if saveJson:
            dump_dir = "jsonDump"
            if not os.path.exists(dump_dir):
                os.mkdir(dump_dir)
                logging.info("Created %s directory" % (dump_dir))
            if not os.path.isdir(dump_dir):
                logging.error("%s is not a directory" % (dump_dir))
            else:
                for i in range(len(blocks)):
                    filename = os.path.join(dump_dir, ".".join([os.path.basename(f), str(i), "json"])) 
                    with open(filename, "w+") as outFile:
                        json.dump(blocks[i], outFile)
                        logging.info("Created Json dump file %s" % (filename))


        raw = extractRaw(blocks)
        rawReplay.append(";".join([os.path.abspath(f), raw[1]])) # add replay line
        rawPlayer.extend([";".join([os.path.abspath(f), line]) for line in raw[0]]) # add players lines
        logging.info("Finished raw extraction from %s blocks" % (f))

    logging.info("Finished directory raw extraction from %s" % (directory))
    return (rawReplay, rawPlayer)


if __name__ == "__main__":
    import sys
    logging.basicConfig(filename="replayAnalize.log", filemode="w+", level=logging.WARNING)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory containing .wotreplay files")
    parser.add_argument("-j", "--saveJson", action="store_true", help="determinates whether to save json dump or not", default=False)
    args = parser.parse_args()
    rawReplay, rawPlayer = extractRawFromDir(args.directory, saveJson=args.saveJson)
    with open("replay.out", "w+") as out:
        for line in rawReplay:
            out.write(line + "\n")

    with open("player.out", "w+") as out:
        for line in rawPlayer:
            out.write(line + "\n")
