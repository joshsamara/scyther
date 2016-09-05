# -*- coding: utf-8 -*-
"""Ball tests."""

from unittest import TestCase

from scyther.ball import Ball


class TestProperties(TestCase):
    def test_catch_modifier(self):
        self.assertEqual(Ball.poke.catch_modifier, 255)

    def test_animation_modifier(self):
        self.assertEqual(Ball.safari.hp_factor, 12)

    def test_id(self):
        self.assertEqual(Ball.ultra.id, 3)

    def test_is_master_ball(self):
        self.assertFalse(Ball.ultra.is_master_ball)
        self.assertTrue(Ball.master.is_master_ball)