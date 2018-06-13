#!/usr/bin/env python3

from datetime import datetime
from collections import namedtuple
from itertools import groupby

import wotReplayLib.enums


Filter = namedtuple("Filter", ["func", "args"])

# --- replay filters ---
def battle_type_filter(replays, battle_type):
    """"""
    return [replay for replay in replays if replay.battle_type == battle_type]

def replay_battle_result_filter(replays, battle_result):
    """"""
    return [replay for replay in replays if replay.battle_result == battle_result]

def block_count_filter(replays, block_count):
    """"""
    return [replay for replay in replays if replay.block_count == block_count]

def map_filter(replays, map_name):
    """"""
    return [replay for replay in replays if replay.map_name == map_name]

def date_filter(replays, date):
    """"""
    return [replay for replay in replays if datetime.strptime(replay.date_time, "%d.%m.%Y %H:%M:%S").date() == date]

# +++ unique +++
def unique_filter(replays, get_key):
    """"""
    out = [] 
    keys = set()
    for replay in replays:
        key = get_key(replay)
        if key not in keys:
            out.append(replay)
            keys.add(key)
    return out

# --- player record filters ---
def vehicle_filter(player_records, vehicle):
    """"""
    return [player_record for player_record in player_records if player_record.vehicle == vehicle]

def player_battle_result_filter(player_records, battle_result):
    """"""
    return [player_record for player_record in player_records if player_record.battle_result == battle_result]

def team_filter(player_records, team):
    """"""
    return [player_record for player_record in player_records if player_record.team == team]

def tag_filter(player_records, tag):
    """"""
    return [player_record for player_record in player_records if player_record.clan_abbrev == tag]

def battle_count_filter(player_records, min_battles, get_key):
    """"""
    groups = [list(records) for key, records in groupby(sorted(player_records, key=get_key), key=get_key)]
    result = []
    for group in groups:
        if len(group) >= min_battles:
            result.extend(group)
    return result
