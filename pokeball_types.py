from enum import Enum


class PokeballType(Enum):
    LOVE = "love"
    DREAM = "dream"
    BEAST = "beast"
    MOON = "moon"
    FRIEND = "friend"
    HEAVY = "heavy"
    LURE = "lure"
    FAST = "fast"
    LEVEL = "level"
    SAFARI = "safari"
    SPORT = "sport"
    POKE = "poke"
    GREAT = "great"
    ULTRA = "ultra"
    MASTER = "master"
    PREMIER = "premier"
    REPEAT = "repeat"
    TIMER = "timer"
    NEST = "nest"
    NET = "net"
    DIVE = "dive"
    LUXURY = "luxury"
    HEAL = "heal"
    QUICK = "quick"
    DUSK = "dusk"
    CHERISH = "cherish"
    POKE_H = "poke-h"
    GREAT_H = "great-h"
    ULTRA_H = "ultra-h"
    FEATHER = "feather"
    WING = "wing"
    JET = "jet"
    HEAVY_H = "heavy-h"
    LEADEN = "leaden"
    GIGATON = "gigaton"
    ORIGIN = "origin"

    # Usage
    def validate_pokeball(ball):
        """
        Validate pokeball.

        Args:
            ball (str): the pokeball to validate
        """
        if not isinstance(ball, str):
            raise TypeError("Pokeball must be a string.")
        return ball in PokeballType
