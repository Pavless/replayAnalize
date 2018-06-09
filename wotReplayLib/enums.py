#!/usr/bin/env python3

from enum import Enum


class MyEnum(Enum):

    def __str__(self):
        return self.name

class BattleResult(MyEnum):
    DRAW=0
    VICTORY=1
    DEFEAT=2
    UNKNOWN=3

    @staticmethod
    def from_string(s):
        try:
            return BattleResult[s]
        except KeyError:
            raise ValueError()

class FinishReason(MyEnum):
    UNKNOWN=0
    EXTERMINATION=1
    BASECAPTURE=2
    TIMEOUT=3
    FAILURE=4
    TECHNICAL=5

    @staticmethod
    def from_string(s):
        try:
            return FinishReason[s]
        except KeyError:
            raise ValueError()

class DeathReason(MyEnum):
    ALIVE=-1
    SHOT=0
    FIRE=1
    RAMMING=2
    CRASHED=3
    DEATHZONE=4
    DROWNED=5

    @staticmethod
    def from_string(s):
        try:
            return DeathReason[s]
        except KeyError:
            raise ValueError()

class Team(MyEnum):
    ALLY=0
    ENEMY=1

    @staticmethod
    def from_string(s):
        try:
            return Team[s]
        except KeyError:
            raise ValueError()


class BattleType(MyEnum):
    REGULAR=1
    SKIRMISH=10
    BATTLEFORSTRONGHOLD=11
    GLOBALMAP=13

    @staticmethod
    def from_string(s):
        try:
            return BattleType[s]
        except KeyError:
            raise ValueError()

