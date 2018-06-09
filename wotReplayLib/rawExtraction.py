#!/usr/bin/env python3

import logging
from .enums import BattleResult
from .enums import Team

def extractRaw(blocks, extractPlayers=True):
    """Extracts the useful informations for each player who participated in the battle and info about the battle itself
    
    blocks: json blocks
    Returns: (list describing battle, List of lines, line foreach player"""

    if len(blocks) != 1 and len(blocks) != 2:
        logging.warning("Unexpected number of data blocks of %i" % (len(blocks)))

    battleRecord = ""
    playerRecords = {}
    if len(blocks) > 0:
        # process matchStart block
        matchStart = blocks[0]
        
        # get owner team
        owner_team = ""
        for vehicleNo, vehicle in matchStart['vehicles'].items():
            if vehicle['name'] == matchStart['playerName']:
                owner_team = vehicle['team']
                break

        if owner_team == "":
            logging.error("Unable to get replay owner team")

        battleRecord = ";".join([str(item) for item in [len(blocks), matchStart['dateTime'], matchStart['mapName'], matchStart['battleType'], matchStart['playerName'], matchStart['playerID'], matchStart['playerVehicle'], owner_team]])
        
        
        for vehicleNo, vehicle in matchStart['vehicles'].items():
            if vehicle['team'] == owner_team:
                team = Team.ALLY
            else:
                team = Team.ENEMY
            playerRecords[vehicleNo] = ";".join([str(item) for item in [len(blocks), matchStart['dateTime'], matchStart['mapName'], matchStart['battleType'], vehicle['name'], vehicle['clanAbbrev'], vehicle['vehicleType'], team.value]])
        try:
            if len(blocks) > 1:
                battleResult = blocks[1][0]
                winner_team = battleResult['common']['winnerTeam']
                if winner_team == owner_team:
                    battleRecord = battleRecord + ";" + str(BattleResult.WIN.value)
                elif winner_team != 0:
                    battleRecord = battleRecord + ";" + str(BattleResult.DEFEAT.value)
                else:
                    battleRecord = battleRecord + ";" + str(BattleResult.DRAW.value)

                battleRecord = battleRecord + ";" + ";".join([str(item) for item in [battleResult['common']['duration'], battleResult['common']['finishReason'], battleResult['arenaUniqueID']]])
                
                if extractPlayers:
                    for vehicleNo, vehicle in battleResult['vehicles'].items():
                        firstVehicle = vehicle[0]
                
                        if vehicleNo not in playerRecords:
                            logging.warning("Unmached vehicleNo %s in battle result block" % (vehicleNo))
                        else:
                            if winner_team == firstVehicle['team']:
                                player_result = BattleResult.WIN
                            elif winner_team != 0:
                                player_result = BattleResult.DEFEAT
                            else:
                                player_result = BattleResult.DRAW
                            playerRecords[vehicleNo] = playerRecords[vehicleNo] + ";" + ";".join([str(item) for item in [player_result.value, battleResult['common']['duration'], battleResult['common']['finishReason'], firstVehicle['accountDBID'], firstVehicle['lifeTime'], firstVehicle['spotted'], firstVehicle['kills'], firstVehicle['tkills'], firstVehicle['damaged'], firstVehicle['tdamageDealt'], firstVehicle['damageAssistedTrack'], firstVehicle['damageAssistedRadio'], firstVehicle['damageAssistedStun'], firstVehicle['damageDealt'], firstVehicle['sniperDamageDealt'], firstVehicle['stunned'], firstVehicle['stunDuration'], firstVehicle['shots'], firstVehicle['piercings'], firstVehicle['damageBlockedByArmor'], firstVehicle['potentialDamageReceived'], firstVehicle['xp'], firstVehicle['droppedCapturePoints'], firstVehicle['deathReason'], firstVehicle['capturePoints'], firstVehicle['mileage']]])

            

        except KeyError:
            logging.error("Unable to extract data from battle result block")

    return (playerRecords.values(), battleRecord)
     
