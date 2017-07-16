# -*- coding: utf-8 -*-
"""Ball tests."""

from unittest import TestCase

from scyther.ball import Ball


class TestProperties(TestCase):
    def test_catch_modifier(self):
        self.assertEqual(Ball.POKE.catch_modifier, 255)

    def test_animation_modifier(self):
        self.assertEqual(Ball.SAFARI.hp_factor, 12)

    def test_display(self):
        self.assertEqual(Ball.ULTRA.display, "Ultraball")

    def test_is_master_ball(self):
        self.assertFalse(Ball.ULTRA.is_master_ball)
        self.assertTrue(Ball.MASTER.is_master_ball)
