# -*- coding: utf-8 -*-
"""Base class representing a single Pokemon.

Made to be generic and loadable with a pokemon's stats.

Note:
    These mechanics mirror generation 1 (RBY).
"""

from random import randint


class Pokemon(object):
    """Generic wild Pokemon.

    Args:
        base_hp (int): The base hp stat.
        hp_ivs (int optional): IVs of the HP stat. If not given will be
            calculated using the same method as Gen I games.
        level (int optional): Current pokemon level. Defaults to 1.
        name (str optional): Pokemon name. Defaults to "Pokemon"
        art (str optional): Ascii art represnting the pokemon.
            Defaults to a pokeball.

    Attributes:
        hp (int): Pokemon's max hit points based on level.
        name (str optional): Name of the pokemon.
    """
    def __init__(self, base_hp, hp_ivs=None, level=1, name="Pokemon"):
        if hp_ivs is None:
            hp_ivs = self.get_hp_ivs()

        self.hp = self.calculate_hp(base_hp, hp_ivs, level)

    @staticmethod
    def get_hp_ivs():
        """Randomly generate a value for HP IVs.

        Notes:
            This micics the actual HP IV calculation.
        """
        attack = (randint(0, 15) & 0b1) << 3
        defense = (randint(0, 15) & 0b1) << 2
        speed = (randint(0, 15) & 0b1) << 1
        special = (randint(0, 15) & 0b1) << 0
        hp = attack | defense | speed | special
        return hp

    @staticmethod
    def calculate_hp(base_hp, hp_ivs, level):
        """Calculate the current max HP.

        See: http://cdn.bulbagarden.net/upload/d/d4/HP_calc.png
        """
        return (((base_hp + hp_ivs) * 2) * level) // 100 + level + 10
