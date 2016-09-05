# -*- coding: utf-8 -*-
"""Tests for Pokemon class."""

from unittest import TestCase, mock

from scyther.pokemon import Pokemon, Status


class TestGetHpIVs(TestCase):
    @mock.patch('scyther.pokemon.randint')
    def test_min_value(self, mock_rand):
        mock_rand.return_value = 0
        self.assertEqual(Pokemon.get_hp_ivs(), 0)
        # All even values should result in 0
        mock_rand.return_value = 2
        self.assertEqual(Pokemon.get_hp_ivs(), 0)
        mock_rand.return_value = 8
        self.assertEqual(Pokemon.get_hp_ivs(), 0)

    @mock.patch('scyther.pokemon.randint')
    def test_max_value(self, mock_rand):
        mock_rand.return_value = 15
        self.assertEqual(Pokemon.get_hp_ivs(), 15)
        # All odd values should result in 15
        mock_rand.return_value = 1
        self.assertEqual(Pokemon.get_hp_ivs(), 15)
        mock_rand.return_value = 7
        self.assertEqual(Pokemon.get_hp_ivs(), 15)

    def test_randoms(self):
        for i in range(1000):
            # Technically this could miss a case where it generates outside
            # But the idea is to hopefully catch any obvious failures.
            # Testing random is hard.
            hp_ivs = Pokemon.get_hp_ivs()
            self.assertGreaterEqual(hp_ivs, 0)
            self.assertLessEqual(hp_ivs, 15)


class TestCalculateHP(TestCase):
    def test_minimum(self):
        """Test impossible minimum case."""
        self.assertEqual(Pokemon.calculate_hp(0, 0, 1), 11)

    def test_diglett(self):
        """Test min base hp pokemon."""
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

    def test_chansey(self):
        """Test max base hp pokemon."""
        self.assertEqual(Pokemon.calculate_hp(250, 0, 1), 16)
        self.assertEqual(Pokemon.calculate_hp(250, 15, 1), 16)
        self.assertEqual(Pokemon.calculate_hp(250, 0, 50), 310)
        self.assertEqual(Pokemon.calculate_hp(250, 15, 50), 325)
        self.assertEqual(Pokemon.calculate_hp(250, 0, 100), 610)
        self.assertEqual(Pokemon.calculate_hp(250, 15, 100), 640)


class TestInit(TestCase):
    def test_name(self):
        self.assertEqual(Pokemon(0).name, "Pokemon")
        # Name should just pass through
        self.assertEqual(Pokemon(0, name="Scyther").name, "Scyther")

    @mock.patch('scyther.pokemon.Pokemon.get_hp_ivs')
    def test_get_hp_ivs(self, mock_ivs):
        """Test that we only call get_hpi_ivs when no hp_ivs are passed in."""
        # Create a new pokemon while passing IVs
        test_pokemon1 = Pokemon(0, hp_ivs=10)
        self.assertFalse(mock_ivs.called)
        self.assertEqual(test_pokemon1._hp_ivs, 10)

        # Passing no IVs will cause get_hp_ivs to be called
        mock_ivs.return_value = 999
        test_pokemon2 = Pokemon(0)
        self.assertTrue(mock_ivs.called)
        self.assertEqual(test_pokemon2._hp_ivs, 999)

    @mock.patch('scyther.pokemon.Pokemon.calculate_hp')
    def test_max_hp(self, mock_calc_hp):
        """Max HP should simply be set as the result of calculate_hp."""
        mock_calc_hp.return_value = 99999
        test_pokemon = Pokemon(0)
        self.assertEqual(test_pokemon.max_hp, 99999)

    def test_status(self):
        # Should default to normal
        test_pokemon1 = Pokemon(0)
        self.assertEqual(test_pokemon1.status, Status.normal)

        # Should use whatever's passed in
        test_pokemon1 = Pokemon(0, status="burned")
        self.assertEqual(test_pokemon1.status, Status.burned)
