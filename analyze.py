#!/usr/bin/env python3

import logging
import argparse
import os
from datetime import datetime

import wotReplayLib.types
import wotReplayLib.enums
import wotReplayLib.filters
from wotReplayLib.types import Replay

def analyze(directory, replay_filters, player_filters):
    """replay_filters.item = (func, args)"""
    replay_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".wotreplay")]
    
    # load replays
    replays = [Replay(f) for f in replay_files]

    # filter replays
    for replay_filter, args in replay_filters:
        replays = replay_filter(replays, *args)

    # filter player records
    for player_filter in player_filters:
        pass
    
    for replay in replays:
        print(replay.file_path)


def validate_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: %s" % (s)
        raise argparse.ArgumentTypeError(msg)

def validate_directory(s):
    if os.path.isdir(s):
        return s
    else:
        msg = "Not a valid directory: %s" % (s)
        raise argparse.ArgumentTypeError(msg)

if __name__ == "__main__":
    logging.basicConfig(filename="analyze.log", filemode="w", level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="the location of .wotreplay files to analyze", type=validate_directory)
    block_group = parser.add_mutually_exclusive_group()
    block_group.add_argument("-i", "--incomplete", help="take only incomplete replays", action="store_true")
    block_group.add_argument("-c", "--complete", help="take only complete replays", action="store_true")
    block_group.add_argument("-u", "--unique", help="take each battle only once, only complete replays", action="store_true")
    parser.add_argument("-m", "--map", help="take only those records which are from the specified map")
    parser.add_argument("-d", "--date", help="take only those records which were played on the specified date, format: YYYY-MM-DD", type=validate_date)
    parser.add_argument("-p", "--players", help="create dump for each player", action="store_true")
    parser.add_argument("-r", "--replay", help="create dump json for each replay", action="store_true")
    parser.add_argument("-t", "--tag", help="take only those player records where the player has the specified clan tag")
    parser.add_argument("-T", "--team", help="take only those player record where the player is on the selected side", type=wotReplayLib.enums.Team, choices=list(wotReplayLib.enums.Team))
    parser.add_argument("-R", "--result", help="take only those player records where the player has the specified battle result", type=wotReplayLib.enums.BattleResult.from_string, choices=list(wotReplayLib.enums.BattleResult))
    parser.add_argument("-v", "--vehicle", help="take only those player records where the player is in the specified vehicle")

    args = parser.parse_args()

    replay_filters = []
    player_filters = []

    # --- replay filters ---
    if args.incomplete:
        replay_filters.append((wotReplayLib.filters.block_count_filter, [1]))
    elif args.complete:
        replay_filters.append((wotReplayLib.filters.block_count_filter, [2]))
    elif args.unique:
        replay_filters.append((wotReplayLib.filters.block_count_filter, [2]))
        replay_filters.append((wotReplayLib.filters.unique_filter, [lambda replay: replay.id]))

    if args.map != None:
        replay_filters.append((wotReplayLib.filters.map_filter, [args.map]))
    if args.date != None:
        replay_filters.append((wotReplayLib.filters.date_filter, [args.date]))
    
    # --- player record filters ---
    if args.tag != None:
        player_filters.append((tag_filter, [args.tag]))
    
    if args.team != None:
        player_filters.append((team_filter, [args.team]))

    if args.result != None:
        player_filters.append((player_battle_result_filter, [args.result]))

    if args.vehicle != None:
        player_filters.append((vehicle_filter, [args.vehicle]))

    analyze(args.directory, replay_filters=replay_filters, player_filters=player_filters)
