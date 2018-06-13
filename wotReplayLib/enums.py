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

    @staticmethod
    def from_value(v):
        try:
            return BattleResult(v)
        except ValueError:
            return BattleResult.UNKNOWN

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

    @staticmethod
    def from_value(v):
        try:
            return FinishReason(v)
        except ValueError:
            return FinishReason.UNKNOWN

class DeathReason(MyEnum):
    ALIVE=-1
    SHOT=0
    FIRE=1
    RAMMING=2
    CRASHED=3
    DEATHZONE=4
    DROWNED=5
    UNKNOWN=1000

    @staticmethod
    def from_string(s):
        try:
            return DeathReason[s]
        except KeyError:
            raise ValueError()

    @staticmethod
    def from_value(v):
        try:
            return DeathReason(v)
        except ValueError:
            return DeathReason.UNKNOWN

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
    UNKNOWN=1000

    @staticmethod
    def from_string(s):
        try:
            return BattleType[s]
        except KeyError:
            raise ValueError()

    @staticmethod
    def from_value(v):
        try:
            return BattleType(v)
        except ValueError:
            return BattleType.UNKNOWN
