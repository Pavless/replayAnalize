#!/usr/bin/env python3

import wotReplayLib.enum
import datetime

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
