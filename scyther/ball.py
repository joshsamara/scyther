# -*- coding: utf-8 -*-
"""Pokeballs used to capture pokemon."""

from enum import Enum


class Ball(Enum):
    """Posible pokeball types.

    The value of the pokeballs are a tuple of integers in the form of:
        (<Effect on Catch/Animation>, <HP Factor>, <Display value>)
    """
    POKE = (255, 12, "Pokeball")
    GREAT = (200, 8, "Greatball")
    ULTRA = (150, 12, "Ultraball")
    SAFARI = (150, 12, "Safariball")
    MASTER = (0, 1, "Masterball")

    def __init__(self, catch_modifier, hp_factor, display):
        self.catch_modifier = catch_modifier
        self.hp_factor = hp_factor
        self.display = display

    @property
    def is_master_ball(self):
        """Is this ball a master ball."""
        return self.name == 'MASTER'
