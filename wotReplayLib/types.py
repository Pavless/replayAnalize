#!/usr/bin/env python3

import logging
import json
import wotReplayLib.enums

from pathlib import Path

class Replay:
    """"""
    def __init__(self, f):
        """"""
        # save file_path
        if isinstance(f, Path):
            self.file_path = f
        elif isinstance(f, str):
            self.file_path = Path(f)
        else:
            raise TypeError("Argument f has to be of Path or str type")
        
        self.player_records = {}
        # +++ analize the replay +++
        # --- get json blocks ---
        
        logging.info("Processing %s" % (str(self.file_path)))
        with open(str(self.file_path), "rb") as opened_file:
            # read magic number
            magic_number = int.from_bytes(opened_file.read(4), byteorder="little")
            logging.debug("Magic number: %i" % (magic_number))
            if magic_number != 288633362:
                logging.warning("Magic number has an unexpected value of %i" % (magic_number))

            # read the block count
            self.block_count = int.from_bytes(opened_file.read(4), byteorder="little")
            logging.debug("Block count: %i" % (self.block_count))

            # read the blocks of json
            self.json_blocks = []
            for i in range(self.block_count):
                # read the block length
                block_length = int.from_bytes(opened_file.read(4), byteorder="little")
                logging.debug("Block no.%i length: %i" % (i, block_length))

                # read the block data
                block = opened_file.read(block_length)
                self.json_blocks.append(json.loads(block.decode("utf-8")))
                logging.info("Block no.%i extracted" % (i))

        # --- get info from match start block ---
        try:
            if self.block_count >= 1:
                logging.info("Starting to read info from match start block")

                match_start = self.json_blocks[0]
                self.author_team_number = None
                for vehicleNo, vehicle in match_start['vehicles'].items():
                    if vehicle['name'] == match_start['playerName']:
                        self.author_team_number = vehicle['team']
                        break

                if self.author_team_number == None:
                    logging.error("Unable to get replay author team")

                self.date_time = match_start['dateTime']
                self.map_name = match_start['mapName']
                self.battle_type = wotReplayLib.enums.BattleType.from_value(match_start['battleType'])
                self.author_name = match_start['playerName']        
                self.author_id = match_start['playerID']
                self.author_vehicle = match_start['playerVehicle']

                for vehicle_no, vehicle in match_start['vehicles'].items():
                    player_record = PlayerRecord()
                    player_record.name = vehicle['name']
                    player_record.clan_abbrev = vehicle['clanAbbrev']
                    player_record.vehicle = vehicle['vehicleType']
                    player_record.team = wotReplayLib.enums.Team.ALLY if vehicle['team'] == self.author_team_number else wotReplayLib.enums.Team.ENEMY
                    self.player_records[vehicle_no] = player_record
        
        except KeyError as e:
            logging.error("In %s, while getting info from match start block KeyError: %s" % (str(self.file_path), str(e)))

        # --- get info from battle result block ---
        try:
            if self.block_count >= 2:
                logging.info("Starting to read info from battle result block")

                battle_result = self.json_blocks[1][0]
                self.winner_team_number = battle_result['common']['winnerTeam']
                if self.winner_team_number == 0:
                    self.battle_result = wotReplayLib.enums.BattleResult.DRAW
                elif self.winner_team_number == self.author_team_number:
                    self.battle_result = wotReplayLib.enums.BattleResult.VICTORY
                else:
                    self.battle_result = wotReplayLib.enums.BattleResult.DEFEAT
                
                self.duration = battle_result['common']['duration']
                self.finish_reason = wotReplayLib.enums.FinishReason.from_value(battle_result['common']['finishReason'])
                self.id = battle_result['arenaUniqueID']

                for vehicle_no, vehicles in battle_result['vehicles'].items():
                    if vehicle_no not in self.player_records:
                        logging.warning("Unmatched vehicle_no %s" % (vehicle_no))
                    else:
                        if len(vehicles) == 0:
                            logging.warning("Empty vehicles for vehicle_no %s" % (vehicle_no))
                        elif len(vehicles) > 1:
                            logging.warning("More vehicles for vehicle_no %s, taking first only the first vehicle" % (str(vehicle_no)))
                        if len(vehicles) >= 1:
                            player_record = self.player_records[vehicle_no]
                            vehicle = vehicles[0]
                            if self.winner_team_number == 0:
                                player_record.battle_result = wotReplayLib.enums.BattleResult.DRAW
                            elif self.winner_team_number == vehicle['team']:
                                player_record.battle_result = wotReplayLib.enums.BattleResult.VICTORY
                            else:
                                player_record.battle_result = wotReplayLib.enums.BattleResult.DEFEAT
                            
                            player_record.id = vehicle['accountDBID']
                            player_record.life_time = vehicle['lifeTime']
                            player_record.spots = vehicle['spotted']
                            player_record.kills = vehicle['kills']
                            player_record.stuns = vehicle['stunned']
                            player_record.stun_duration = vehicle['stunDuration']
                            player_record.team_kills = vehicle['tkills']
                            player_record.vehicles_damaged = vehicle['damaged']
                            player_record.damage = vehicle['damageDealt']
                            player_record.sniper_damage = vehicle['sniperDamageDealt']
                            player_record.team_damage = vehicle['tdamageDealt']
                            player_record.assist_track = vehicle['damageAssistedTrack']
                            player_record.assist_spot = vehicle['damageAssistedRadio']
                            player_record.assist_stun = vehicle['damageAssistedStun']
                            player_record.shots = vehicle['shots']
                            player_record.piercings = vehicle['piercings']
                            player_record.damage_blocked = vehicle['damageBlockedByArmor']
                            player_record.damage_potential = vehicle['potentialDamageReceived']
                            player_record.xp = vehicle['xp']
                            player_record.points_dropped = vehicle['droppedCapturePoints']
                            player_record.points_capture = vehicle['capturePoints']
                            player_record.death_reason = wotReplayLib.enums.DeathReason.from_value(vehicle['deathReason'])
                            player_record.milage = vehicle['mileage']
                            
        
        except KeyError as e:
            logging.error("In %s, while getting info from battle result block KeyError: %s" % (str(self.file_path), str(e)))



class PlayerRecord:
    """"""
    def __init__(self):
        """"""
        # --- match start ---
        self.name = None
        self.clan_abbrev = None
        self.vehicle = None
        self.team = None

        # --- battle result ---
        self.battle_result = None
        self.id = None
        self.life_time = None
        self.spots = None
        self.kills = None
        self.stuns = None
        self.stun_duration = None
        self.team_kills = None
        self.vehicles_damaged = None
        self.damage = None
        self.sniper_damage = None
        self.team_damage = None
        self.assist_track = None
        self.assist_spot = None
        self.assist_stun = None
        self.shots = None
        self.piercings = None
        self.damage_blocked = None
        self.damage_potential = None
        self.xp = None
        self.points_dropped = None
        self.points_capture = None
        self.death_reason = None
        self.milage = None
