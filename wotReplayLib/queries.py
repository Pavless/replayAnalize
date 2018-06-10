#!/usr/bin/env python3

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

def top_stat(player_records, stat_selector, group_by, n=10):
    return (list(reversed(sorted(player_records, key=stat_selector))))[:n]

def top_avg_stat(player_records, stat_selector, group_by, n=10):
    

def worst_stat(player_records, stat_selector, group_by, n=10):
    return (list(sorted(player_records, key=stat_selector)))[:n]

def worst_avg_stat(player_records, stat_selector, group_by, n=10):
    pass
