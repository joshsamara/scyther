# -*- coding: utf-8 -*-
"""A representation of a single pokemon.

Made to be generic and loadable with a pokemon's stats.

Note:
    These mechanics mirror generation 1 (RBY).
"""

from random import randint

from scyther.status import Status, InvalidStatusError


class Pokemon(object):
    """Generic wild Pokemon.

    Args:
        base_hp (int): The base hp stat.
        hp_ivs (int optional): IVs of the HP stat. If not given will be
            calculated using the same method as Gen I games.
        level (int optional): Current pokemon level. Defaults to 1.
        status (string optional): String representing the current status.
            Maps to a member of the Status enum. Defaults to normal
        catch_rate (int optional): The pokemon's catch rate.
        name (str optional): Pokemon name. Defaults to "Pokemon"
        is_ghost_marowak (boolean optional): Is this pokemon Ghost Marowak?
        art (str optional): Ascii art represnting the pokemon.
            Defaults to a pokeball. TODO

    Attributes:
        max_hp (int): Pokemon's max hit points based on level.
        level (int): Pokemon's current level.
        catch_rate (int): Pokemon's catch rate.
        status (Status): Pokemon's current status.
        name (str): Name of the pokemon.
        is_ghost_marowak (boolean): Is this pokemon Ghost Marowak?
    """
    def __init__(self, base_hp, hp_ivs=None, level=1,
                 catch_rate=255, status="normal", name="Pokemon",
                 is_ghost_marowak=False):
        if hp_ivs is None:
            hp_ivs = self.get_hp_ivs()

        self.max_hp = self.calculate_hp(base_hp, hp_ivs, level)
        self.level = level
        self.catch_rate = catch_rate
        self.status = self.get_status(status)
        self.name = name
        self.is_ghost_marowak = is_ghost_marowak
        # Set private attributes for debugging/testing
        self._base_hp = base_hp
        self._hp_ivs = hp_ivs

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
        hp_ivs = attack | defense | speed | special
        return hp_ivs

    @staticmethod
    def calculate_hp(base_hp, hp_ivs, level):
        """Calculate the current max HP.

        See: http://cdn.bulbagarden.net/upload/d/d4/HP_calc.png
        """
        return (((base_hp + hp_ivs) * 2) * level) // 100 + level + 10

    @staticmethod
    def get_status(status):
        """Get a member of a Status enum from a status string."""
        try:
            return Status[status]
        except KeyError:
            raise InvalidStatusError(status)
