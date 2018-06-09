#!/usr/bin/env python3

from enum import Enum


class MyEnum(Enum):

    def __str__(self):
        return self.name

class BattleResult(MyEnum):
    DRAW=0
    WIN=1
    DEFEAT=2
    UNKNOWN=3

    @staticmethod
    def fromString(s):
        try:
            return BattleResult[s]
        except KeyError:
            raise ValueError()


class Team(MyEnum):
    ALLY=0
    ENEMY=1

    @staticmethod
    def fromString(s):
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
    def fromString(s):
        try:
            return BattleType[s]
        except KeyError:
            raise ValueError()

