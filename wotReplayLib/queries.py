#!/usr/bin/env python3

import statistics
from collections import namedtuple
from itertools import groupby

# ==== stat list ====
# damage
# kills
# assistance
# assistance spot
# assistance stun
# assistance track
# team kills
# xp
# spots
# win rate
# survival rate

def highest_stat(player_records, stat_selector):
    return reversed(sorted(player_records, key=stat_selector))

def lowest_stat(player_records, stat_selector):
    return sorted(player_records, key=stat_selector)

def avg_stat(player_records, stat_selector):
    return statistics.mean([stat_selector(record) for record in player_records])

def total_stat(player_records, stat_selector):
    return sum([stat_selector(record) for record in player_records])
