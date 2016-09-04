# -*- coding: utf-8 -*-
"""Tests for Pokemon class."""

import unittest
from scyther.pokemon import Pokemon


class TestGetHpIVs(unittest.TestCase):
    @unittest.skip("TODO")
    def test_nothing(self):
        self.assertEqual(Pokemon.get_hp_ivs(), 0)


class TestCalculateHP(unittest.TestCase):
    def test_minimum(self):
        self.assertEqual(Pokemon.calculate_hp(0, 0, 1), 11)

    def test_diglett(self):
        """Test min base hp edge case."""
        self.assertEqual(Pokemon.calculate_hp(10, 0, 1), 11)
        self.assertEqual(Pokemon.calculate_hp(10, 15, 1), 11)
        self.assertEqual(Pokemon.calculate_hp(10, 0, 50), 70)
        self.assertEqual(Pokemon.calculate_hp(10, 15, 50), 85)
        self.assertEqual(Pokemon.calculate_hp(10, 0, 100), 130)
        self.assertEqual(Pokemon.calculate_hp(10, 15, 100), 160)

    def test_scyther(self):
        """Test scyther case."""
        self.assertEqual(Pokemon.calculate_hp(70, 0, 1), 12)
        self.assertEqual(Pokemon.calculate_hp(70, 15, 1), 12)
        self.assertEqual(Pokemon.calculate_hp(70, 0, 50), 130)
        self.assertEqual(Pokemon.calculate_hp(70, 15, 50), 145)
        self.assertEqual(Pokemon.calculate_hp(70, 0, 100), 250)
        self.assertEqual(Pokemon.calculate_hp(70, 15, 100), 280)

    def test_chancey(self):
        """Test max base hp edge case."""
        self.assertEqual(Pokemon.calculate_hp(250, 0, 1), 16)
        self.assertEqual(Pokemon.calculate_hp(250, 15, 1), 16)
        self.assertEqual(Pokemon.calculate_hp(250, 0, 50), 310)
        self.assertEqual(Pokemon.calculate_hp(250, 15, 50), 325)
        self.assertEqual(Pokemon.calculate_hp(250, 0, 100), 610)
        self.assertEqual(Pokemon.calculate_hp(250, 15, 100), 640)
