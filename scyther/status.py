# -*- coding: utf-8 -*-
"""Pokemon status effects."""

from enum import Enum


class Status(Enum):
    """Posible pokemon statuses.

    The value of the status are a tuple of integers in the form of:
        (<Effect on catch chance>, <Effect on animation chance>, <Display value>)
    """
    normal = (0, 0, "Normal")
    poisoned = (0, 5, "Poisoned")
    burned = (12, 5, "Burned")
    paralyzed = (12, 5, "Paralyzed")
    asleep = (25, 10, "Asleep")
    frozen = (25, 10, "Frozen")

    @property
    def catch_modifier(self):
        """Modifier of the Status on the catch chance."""
        return self.value[0]

    @property
    def animation_modifier(self):
        """Modifier of the Status on the animation effect."""
        return self.value[1]

    @property
    def display(self):
        """The Status's display value."""
        return self.value[2]
