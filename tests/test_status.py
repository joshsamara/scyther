# -*- coding: utf-8 -*-
"""Status tests."""

from unittest import TestCase

from scyther.status import Status


class TestProperties(TestCase):
    def test_catch_modifier(self):
        self.assertEqual(Status.burned.catch_modifier, 12)

    def test_animation_modifier(self):
        self.assertEqual(Status.asleep.animation_modifier, 10)

    def test_display(self):
        self.assertEqual(Status.frozen.display, "Frozen")
