#!/usr/bin/env python3

import logging
import argparse
import os

import wotReplayLib.types
import wotReplayLib.enums
from wotReplayLib.types import Replay

def analyze(directory, replay_filters, player_filters):
    replay_files = [f for f in os.listdir(directory) if f.endswith(".wotreplay")]
    
    # load replays
    replays = [Replay(f) for f in replay_files]

    # filter replays
    for replay_filter, args in replay_filters:
        replays = replay_filter(replays, *args)

    # filter player records
    for player_filter in player_filters:
        pass



from argparse import ArgumentTypeError
def validate_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: %s" % (s)
        raise ArgumentTypeError(msg)

if __name__ == "__main__":
    logging.basicConfig(filename="analyze.log", filemode="w", level=logging.WARNING)

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="the location of .wotreplay files to analyze")
    block_group = parser.add_mutually_exclusive_group()
    block_group.add_argument("-i", "--incomplete", help="take only incomplete replays", action="store_true")
    block_group.add_argument("-c", "--complete", help="take only complete replays", action="store_true")
    block_group.add_argument("-u", "--unique", help="take each battle only once, only complete replays", action="store_true")
    parser.add_argument("-p", "--players", help="create dump for each player", action="store_true")
    parser.add_argument("-r", "--replay", help="create dump json for each replay", action="store_true")
    parser.add_argument("-t", "--tag", help="take only those player records where the player has the specified clan tag")
    team_group = parser.add_mutually_exclusive_group()
    team_group.add_argument("-a", "--ally", help="take only those player records where the player is in the same team as the replay author", action="store_true")
    team_group.add_argument("-e", "--enemy", help="take only those player records where the player is not in the same team as the replay author", action="store_true")
    parser.add_argument("-m", "--map", help="take only those records which are from the specified map")
    parser.add_argument("-d", "--date", help="take only those records which were played on the specified date, format: YYYY-MM-DD", type=validate_date)
    parser.add_argument("-R", "--result", help="take only those player records where the player has the specified battle result", type=wotReplayLib.enums.BattleResult.from_string)
    parser.add_argumnet("-v", "--vehicle", help="take only those player records where the player is in the specified vehicle")

    args = parser.parse_args()

    replay_filters = set()
    player_filters = set()

