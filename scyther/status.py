# -*- coding: utf-8 -*-
"""Pokemon status effects."""

from enum import Enum


class Status(Enum):
    """Posible pokemon statuses.

    The value of the status are a tuple of integers in the form of:
        (<Effect on catch chance>, <Effect on animation chance>, <Display value>)
    """

    NORMAL = (0, 0, "Normal")
    POISONED = (0, 5, "Poisoned")
    BURNED = (12, 5, "Burned")
    PARALYZED = (12, 5, "Paralyzed")
    ASLEEP = (25, 10, "Asleep")
    FROZEN = (25, 10, "Frozen")

    def __init__(self, catch_modifier: int, animation_modifier: int, display: str) -> None:
        self.catch_modifier = catch_modifier
        self.animation_modifier = animation_modifier
        self.display = display
