# -*- coding: utf-8 -*-
"""A representation of a single pokemon.

Made to be generic and loadable with a pokemon's stats.

Note:
    These mechanics mirror generation 1 (RBY).
"""

from random import randint

from scyther.status import Status


class Pokemon(object):
    """Generic wild Pokemon.

    Args:
        base_hp (int optional): The base hp stat.
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
        current_hp (int): Pokemon's current hit points.
        level (int): Pokemon's current level.
        catch_rate (int): Pokemon's catch rate.
        status (Status): Pokemon's current status.
        name (str): Name of the pokemon.
        is_ghost_marowak (boolean): Is this pokemon Ghost Marowak?
    """
    def __init__(self, base_hp=1, hp_ivs=None, level=1,
                 catch_rate=255, status="normal", name="Pokemon",
                 is_ghost_marowak=False):
        if hp_ivs is None:
            hp_ivs = self.get_hp_ivs()

        self.max_hp = self.calculate_hp(base_hp, hp_ivs, level)
        self.current_hp = self.max_hp
        self.level = level
        self.catch_rate = catch_rate
        self.status = Status[status]
        self.name = name
        self.is_ghost_marowak = is_ghost_marowak
        # Set private attributes for debugging/testing
        self._base_hp = base_hp
        self._hp_ivs = hp_ivs

    @staticmethod
    def get_hp_ivs():
        """Randomly generate a value for HP IVs.

        Notes:
            This mimcics the actual HP IV calculation.
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

    def catch(self, ball):
        """Attempt to catch a pokemon with a given ball.

        Args:
            ball (Ball): Ball being used to catch a pokemon.

        Returns:
            bool: Whether or not the pokemon was caught.

        Notes:
            The checks and logic here mimic the checks from the original game.
        """
        # Ghost Marowak can't be caught.
        if self.is_ghost_marowak:
            return False
        # Masterballs will always catch.
        if ball.is_master_ball:
            return True

        # Create a check value based off the ball and Pokemon's status.
        ballcheck = self._catch_ballcheck(ball)
        # If the first check value is less than 0 catch immediately.
        if ballcheck < 0:
            return True
        # If the pokemon's catch rate is greater then the catch value,
        # release immediately.
        if self.catch_rate < ballcheck:
            return False

        # Create a check value based of the pokemon's current hp and the ball.
        hpcheck = self._catch_hpcheck(ball)
        # Compare to a random integer between 0, 255.
        if randint(0, 255) <= hpcheck:
            return True

        # If we haven't caught at this point, the catch failed failed.
        return False

    ##
    # Catch utility functions
    #
    # These are defined outside of the catch function for better testability.
    ##
    def _catch_ballcheck(self, ball):
        """
        Calculate the ballcheck for the catch function.


        Note:
            A lower value here increases catch rate.
        """
        return randint(0, ball.catch_modifier) - self.status.catch_modifier

    def _catch_hpcheck(self, ball):
        """
        Calculate the hp check for the catch function.

        Note:
            A lower value here lowers catch rate.
        """
        hp_check = self.max_hp * 255
        hp_check //= ball.hp_factor
        hp_divisor = self.current_hp // 4
        if hp_divisor > 0:
            hp_check = hp_check // hp_divisor
        return min(hp_check, 255)
