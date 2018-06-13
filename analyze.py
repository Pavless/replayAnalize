#!/usr/bin/env python3

import logging
import argparse
import os
from datetime import datetime
from itertools import groupby
from itertools import islice
from collections import namedtuple
import statistics

import wotReplayLib.types
from wotReplayLib import enums
from wotReplayLib import filters
from wotReplayLib import queries
from wotReplayLib.types import Replay
from wotReplayLib.filters import Filter

def analyze(directory, replay_filters, player_filters):
    """replay_filters.item = Filter(func, args)"""
    replay_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".wotreplay")]
    
    # load replays
    replays = [Replay(f) for f in replay_files]
    logging.debug("Loaded %i replay files" % (len(replays)))

    # filter replays
    for replay_filter in replay_filters:
        replays = replay_filter.func(replays, *replay_filter.args)
    logging.debug("Replay filters finished, %i replay files left" % (len(replays)))

    # get player records
    player_records = list() 
    for replay in replays:
        player_records.extend(replay.player_records.values())

    logging.debug("Loaded %i player records" % (len(player_records)))

    # filter player records
    for player_filter in player_filters:
        player_records = player_filter.func(player_records, *player_filter.args)

    logging.debug("Player filters finished, %i player records left" % (len(player_records)))

    # ==== stat list ====
    # damage
    # kills
    # assistance
    # assistance spot
    # assistance stun
    # assistance track
    # team kills
    # team damage
    # xp
    # spots
    # win rate
    # survival rate
    StatQuery = namedtuple("StatQuery", "name get_stat")
    stat_queries = []
    stat_queries.append(StatQuery("damage", lambda r: r.damage))
    stat_queries.append(StatQuery("kills", lambda r: r.kills))
    stat_queries.append(StatQuery("assistance", lambda r: r.assist_track + r.assist_spot + r.assist_stun))
    stat_queries.append(StatQuery("spot assistance", lambda r: r.assist_spot))
    stat_queries.append(StatQuery("stun assistance", lambda r: r.assist_stun))
    stat_queries.append(StatQuery("track assistance", lambda r: r.assist_track))
    stat_queries.append(StatQuery("team kills", lambda r: r.team_kills))
    stat_queries.append(StatQuery("xp", lambda r: r.xp))
    stat_queries.append(StatQuery("spots", lambda r: r.spots))

    overall_stat_queries = []
    overall_stat_queries.append(StatQuery("battles", lambda records: len(records)))
    overall_stat_queries.append(StatQuery("win rate", lambda records: len([r for r in records if r.battle_result == enums.BattleResult.VICTORY]) / len(records)))
    overall_stat_queries.append(StatQuery("survival rate", lambda records: len([r for r in records if r.death_reason == enums.DeathReason.ALIVE]) / len(records)))

    id_lambda = lambda r: r.id
    id_to_name = dict()
    for record in player_records:
        if record.id not in id_to_name:
            id_to_name[record.id] = record.name
    
    # +++ for each player +++
    d_players_name = "players_stats"
    if os.path.isdir(d_players_name):
        for id, records in groupby(sorted(player_records, key=id_lambda), key=id_lambda):
            records = list(records)
            if len(records) == 0:
                logging.error("Empty records for player id: %i" % (id))
                continue
            with open(os.path.join(d_players_name, records[0].name + ".txt"), "w") as out:
                out.write("%25s: %i\n" % ("ID", id))
                out.write("%25s: %s\n" % ("Player name", records[0].name))
                for query in overall_stat_queries:
                    out.write("%25s: %.2f\n" % (query.name, query.get_stat(records)))
                out.write("\n")
                for query in stat_queries:
                    out.write("%25s: %.2f\n" % ("Average " + query.name, statistics.mean([query.get_stat(record) for record in records])))
                out.write("\n")
                for query in stat_queries:
                    out.write("%25s: %i\n" % ("Total " + query.name, sum([query.get_stat(record) for record in records])))
                out.write("\n")
                for query in stat_queries:
                    out.write("%25s: %i\n" % ("Highest " + query.name, max([query.get_stat(record) for record in records])))
    else:
        logging.error("Missing directory: %s" % (d_players_name))

    n = 10
    def mean_key(values, key):
        values = list(values)
        return sum([key(value) for value in values]) / len(values)

    with open("leaderboard.txt", "w") as out:
        for query in overall_stat_queries:
            out.write("%25s: %s\n" % ("Query","Highest " + query.name))
            groups =[(id, list(records)) for id, records in groupby(sorted(player_records, key=id_lambda), key=id_lambda)]
            groups = [(id, query.get_stat(records)) for id, records in groups]
            groups.sort(key=lambda t: t[1], reverse=True)
            for id, value in islice(groups, n):
                out.write("%25s: %.2f\n" % (id_to_name[id], value))
            out.write("\n")

        for query in stat_queries:
            out.write("%25s: %s\n" % ("Query", "Average " + query.name))
            groups = [(id, statistics.mean([query.get_stat(record) for record in records])) for id, records in groupby(sorted(player_records, key=id_lambda), key=id_lambda)]
            groups.sort(key=lambda t: t[1], reverse=True)
            for id, value in islice(groups, n):
                out.write("%25s: %.2f\n" % (id_to_name[id], value))
            out.write("\n")

            out.write("%25s: %s\n" % ("Query", "Total " + query.name))
            groups = [(id, sum([query.get_stat(record) for record in records])) for id, records in groupby(sorted(player_records, key=id_lambda), key=id_lambda)]
            groups.sort(key=lambda t: t[1], reverse=True)
            for id, value in islice(groups, n):
                out.write("%25s: %i\n" % (id_to_name[id], value))
            out.write("\n")

            out.write("%25s: %s\n" % ("Query", "Highest " + query.name))
            groups = [(id, max([query.get_stat(record) for record in records])) for id, records in groupby(sorted(player_records, key=id_lambda), key=id_lambda)]
            groups.sort(key=lambda t: t[1], reverse=True)
            for id, value in islice(groups, n):
                out.write("%25s: %i\n" % (id_to_name[id], value))
            out.write("\n")


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
    logging.basicConfig(filename="analyze.log", filemode="w", level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="the location of .wotreplay files to analyze", type=validate_directory)
    block_group = parser.add_mutually_exclusive_group()
    block_group.add_argument("-i", "--incomplete", help="take only incomplete replays", action="store_true")
    block_group.add_argument("-c", "--complete", help="take only complete replays", action="store_true")
    block_group.add_argument("-u", "--unique", help="take each battle only once, only complete replays", action="store_true")
    parser.add_argument("-m", "--map", help="take only those records which are from the specified map")
    parser.add_argument("-b", "--battle-type", help="take only those battles with the specified battle type", type=enums.BattleType.from_string, choices=list(enums.BattleType))
    parser.add_argument("-d", "--date", help="take only those records which were played on the specified date, format: YYYY-MM-DD", type=validate_date)
    parser.add_argument("-p", "--players", help="create dump for each player, NOT IMPLEMENTED", action="store_true")
    parser.add_argument("-r", "--replay", help="create dump json for each replay, NOT IMPLEMENTED", action="store_true")
    parser.add_argument("-t", "--tag", help="take only those player records where the player has the specified clan tag")
    parser.add_argument("-T", "--team", help="take only those player record where the player is on the selected side", type=enums.Team.from_string, choices=list(enums.Team))
    parser.add_argument("-R", "--result", help="take only those player records where the player has the specified battle result", type=enums.BattleResult.from_string, choices=list(enums.BattleResult))
    parser.add_argument("-v", "--vehicle", help="take only those player records where the player is in the specified vehicle")
    parser.add_argument("-B", "--min-battles", help="take only those players who have at least certain number of battles", type=int)

    args = parser.parse_args()

    replay_filters = []
    player_filters = []

    # --- replay filters ---
    if args.incomplete:
        replay_filters.append(Filter(filters.block_count_filter, [1]))
    elif args.complete:
        replay_filters.append(Filter(filters.block_count_filter, [2]))
    elif args.unique:
        replay_filters.append(Filter(filters.block_count_filter, [2]))
        replay_filters.append(Filter(filters.unique_filter, [lambda replay: replay.id]))

    if args.map != None:
        replay_filters.append(Filter(filters.map_filter, [args.map]))
    if args.battle_type != None:
        replay_filters.append(Filter(filters.battle_type_filter, [args.battle_type]))
    if args.date != None:
        replay_filters.append(Filter(filters.date_filter, [args.date]))
    
    # --- player record filters ---
    if args.tag != None:
        player_filters.append(Filter(filters.tag_filter, [args.tag]))
    
    if args.team != None:
        player_filters.append(Filter(filters.team_filter, [args.team]))

    if args.result != None:
        player_filters.append(Filter(filters.player_battle_result_filter, [args.result]))

    if args.vehicle != None:
        player_filters.append(Filter(filters.vehicle_filter, [args.vehicle]))

    if args.min_battles != None:
        player_filters.append(Filter(filters.battle_count_filter, [args.min_battles, lambda r: r.name]))

    analyze(args.directory, replay_filters=replay_filters, player_filters=player_filters)
