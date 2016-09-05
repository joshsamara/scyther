# -*- coding: utf-8 -*-
"""Pokeballs used to capture pokemon."""

from enum import Enum


class Ball(Enum):
    """Posible pokeball types.

    The value of the pokeballs are a tuple of integers in the form of:
        (<Effect on Catch/Animation>, <HP Factor>, <Display value>)
    """
    poke = (255, 12, "Pokeball")
    great = (200, 8, "Greatball")
    ultra = (150, 12, "Ultraball")
    safari = (150, 12, "Safariball")
    master = (None, None, "Masterball")

    @property
    def catch_modifier(self):
        """Modifier of the Ball on catch chance/animiation effect."""
        return self.value[0]

    @property
    def hp_factor(self):
        """Modifier of the Ball the HP factor of the catch chance."""
        return self.value[1]

    @property
    def display(self):
        """The ball's display value."""
        return self.value[2]

    @property
    def is_master_ball(self):
        """Is this ball a master ball."""
        return self.name == 'master'
