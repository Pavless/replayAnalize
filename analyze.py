#!/usr/bin/env python3

import logging
import argparse
import os
from datetime import datetime
from itertools import groupby

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

    # +++ for each player +++
    d_players_name = "players_stats"
    if os.path.isdir(d_players_name):
        id_lambda = lambda r: r.id
        for id, records in groupby(sorted(player_records, key=id_lambda), key=id_lambda):
            records = list(records)
            if len(records) == 0:
                logging.error("Empty records for player id: %i" % (id))
                continue
            win_rate = len([r for r in records if r.battle_result == enums.BattleResult.VICTORY]) / len(records)
            survival_rate = len([r for r in records if r.death_reason == enums.DeathReason.ALIVE]) / len(records)
            with open(os.path.join(d_players_name, records[0].name + ".txt"), "w") as out:
                out.write("%25s: %i\n" % ("ID", id))
                out.write("%25s: %s\n" % ("Player name", records[0].name))
                out.write("%25s: %i\n" % ("Battles", len(records)))
                out.write("%25s: %i %%\n" % ("Win rate", win_rate * 100))
                out.write("%25s: %i %%\n" % ("Survival rate", survival_rate * 100))
                out.write("\n")
                out.write("%25s: %.2f\n" % ("Average damage", queries.avg_stat(records, lambda r: r.damage)))
                out.write("%25s: %.2f\n" % ("Average kills", queries.avg_stat(records, lambda r: r.kills)))
                out.write("%25s: %.2f\n" % ("Average assistance", queries.avg_stat(records, lambda r: r.assist_track + r.assist_spot + r.assist_stun)))
                out.write("%25s: %.2f\n" % ("Average spot assistance", queries.avg_stat(records, lambda r: r.assist_spot)))
                out.write("%25s: %.2f\n" % ("Average stun assistance", queries.avg_stat(records, lambda r: r.assist_stun)))
                out.write("%25s: %.2f\n" % ("Average track assistance", queries.avg_stat(records, lambda r: r.assist_track)))
                out.write("%25s: %.2f\n" % ("Average team kills", queries.avg_stat(records, lambda r: r.team_kills)))
                out.write("%25s: %.2f\n" % ("Average team damage", queries.avg_stat(records, lambda r: r.team_damage)))
                out.write("%25s: %.2f\n" % ("Average xp", queries.avg_stat(records, lambda r: r.xp)))
                out.write("%25s: %.2f\n" % ("Average spots", queries.avg_stat(records, lambda r: r.spots)))
                out.write("\n")
                out.write("%25s: %i\n" % ("Total damage", queries.total_stat(records, lambda r: r.damage)))
                out.write("%25s: %i\n" % ("Total kills", queries.total_stat(records, lambda r: r.kills)))
                out.write("%25s: %i\n" % ("Total assistance", queries.total_stat(records, lambda r: r.assist_track + r.assist_spot + r.assist_stun)))
                out.write("%25s: %i\n" % ("Total spot assistance", queries.total_stat(records, lambda r: r.assist_spot)))
                out.write("%25s: %i\n" % ("Total stun assistance", queries.total_stat(records, lambda r: r.assist_stun)))
                out.write("%25s: %i\n" % ("Total track assistance", queries.total_stat(records, lambda r: r.assist_track)))
                out.write("%25s: %i\n" % ("Total team kills", queries.total_stat(records, lambda r: r.team_kills)))
                out.write("%25s: %i\n" % ("Total team damage", queries.total_stat(records, lambda r: r.team_damage)))
                out.write("%25s: %i\n" % ("Total xp", queries.total_stat(records, lambda r: r.xp)))
                out.write("%25s: %i\n" % ("Total spots", queries.total_stat(records, lambda r: r.spots)))
                out.write("\n")
                out.write("%25s: %i\n" % ("Highest damage", next(queries.highest_stat(records, lambda r: r.damage)).damage))
                out.write("%25s: %i\n" % ("Highest kills", next(queries.highest_stat(records, lambda r: r.kills)).kills))
                record =next(queries.highest_stat(records, lambda r: r.assist_track + r.assist_spot + r.assist_stun))
                out.write("%25s: %i\n" % ("Highest assistance", record.assist_track + record.assist_spot + record.assist_stun))
                out.write("%25s: %i\n" % ("Highest spot assistance", next(queries.highest_stat(records, lambda r: r.assist_spot)).assist_spot))
                out.write("%25s: %i\n" % ("Highest stun assistance", next(queries.highest_stat(records, lambda r: r.assist_stun)).assist_stun))
                out.write("%25s: %i\n" % ("Highest track assistance", next(queries.highest_stat(records, lambda r: r.assist_track)).assist_track))
                out.write("%25s: %i\n" % ("Highest team kills", next(queries.highest_stat(records, lambda r: r.team_kills)).team_kills))
                out.write("%25s: %i\n" % ("Highest team damage", next(queries.highest_stat(records, lambda r: r.team_damage)).team_damage))
                out.write("%25s: %i\n" % ("Highest xp", next(queries.highest_stat(records, lambda r: r.xp)).xp))
                out.write("%25s: %i\n" % ("Highest spots", next(queries.highest_stat(records, lambda r: r.spots)).spots))
    else:
        logging.error("Missing directory: %s" % (d_players_name))

    # +++ highest +++

    # +++ lowest +++

    # +++ avg +++

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
        player_filters.append(Filter(wotReplayLib.vehicle_filter, [args.vehicle]))

    analyze(args.directory, replay_filters=replay_filters, player_filters=player_filters)
