# -*- coding: utf-8 -*-
"""Pokemon status effects."""

from enum import Enum


class Status(Enum):
    """Posible pokemon statuses.

    The value of the status are a tuple of integers in the form of:
        (<Effect on catch chance>, <Effect on animation chance>, id)

    Note:
        The id field is set to allow multiple Status of the same chances to
        exist separately in the same Enum.
    """
    normal = (0, 0, 1)
    poisoned = (0, 5, 2)
    burned = (12, 5, 3)
    paralyzed = (12, 5, 4)
    asleep = (25, 10, 5)
    frozen = (25, 10, 6)

    @classmethod
    def names(cls):
        """Get the name of all members of the Status enum."""
        return [member.name for member in cls]
