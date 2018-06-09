#!/usr/bin/env python3

import logging
import json

def extractBlocks(openedFile):
    """Extracts json block of data at the start of the .wotreplay file
    
    Returns: List of text json blocks"""
    # read magic number
    magic_number = int.from_bytes(openedFile.read(4), byteorder="little")
    logging.debug("Magic number: %i" % (magic_number))
    if magic_number != 288633362:
        logging.warning("Magic number has an unexpected value of %i" % (magic_number))

    # read the block count
    block_count = int.from_bytes(openedFile.read(4), byteorder="little")
    logging.debug("Block count: %i" % (block_count))

    # read the blocks of json
    blocks = []
    for i in range(block_count):
        # read the block length
        block_length = int.from_bytes(openedFile.read(4), byteorder="little")
        logging.debug("Block no.%i length: %i" % (i, block_length))

        # read the block data
        block = openedFile.read(block_length)
        blocks.append(json.loads(block.decode("utf-8")))
        logging.info("Block no.%i extracted" % (i))

    return blocks
