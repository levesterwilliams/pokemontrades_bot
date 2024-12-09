# pokeball_types.py
#
# Levester Williams
# 4 May 2024
#
# Platform info:
# - python 3.12.0
#

from enum import Enum
"""
This module contains all the enumerations that can be used to represent the
different types of balls that a Pokemon can be inside as of December 2024.
"""
PokeballType = Enum(
    "PokeballType",
    [
        "LOVE", "DREAM", "BEAST", "MOON", "FRIEND", "HEAVY", "LURE", "FAST",
        "LEVEL", "SAFARI", "SPORT", "POKEBALL", "GREAT", "ULTRA", "MASTER",
        "PREMIER", "REPEAT", "TIMER", "NEST", "NET", "DIVE", "LUXURY",
        "HEAL", "QUICK", "DUSK", "CHERISH", "POKEBALL_H", "GREAT_H",
        "ULTRA_H", "FEATHER", "WING", "JET", "HEAVY_H", "LEADEN",
        "GIGATON", "ORIGIN"
    ]
)


def validate_pokeball(ball: str) -> bool:
    """
    Validate pokeball.

    Args:
        ball (str): the pokeball to validate

       Returns:
        bool: True if ball is an enum
    """
    try:
        PokeballType[ball.upper()]
        return True
    except KeyError:
        return False
