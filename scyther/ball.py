# -*- coding: utf-8 -*-
"""Pokeballs used to capture pokemon."""

from enum import Enum


class Ball(Enum):
    """Posible pokeball types.

    The value of the pokeballs are a tuple of integers in the form of:
        (<Effect on Catch/Animation>, <HP Factor>, id)
    """
    poke = (255, 12, 1)
    great = (200, 8, 2)
    ultra = (150, 12, 3)
    safari = (150, 12, 4)
    master = (None, None, 5)

    @property
    def catch_modifier(self):
        """Modifier of the Ball on catch chance/animiation effect."""
        return self.value[0]

    @property
    def hp_factor(self):
        """Modifier of the Ball the HP factor of the catch chance."""
        return self.value[1]

    @property
    def id(self):
        """The ball's ID."""
        return self.value[2]

    @property
    def is_master_ball(self):
        """Is this ball a master ball."""
        return self.name == 'master'
