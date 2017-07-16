# -*- coding: utf-8 -*-
"""Tests for Pokemon class."""

from unittest import TestCase, mock
from nose_parameterized import parameterized

from scyther.status import Status
from scyther.ball import Ball
from scyther.pokemon import Pokemon


class TestGetHpIVs(TestCase):
    @mock.patch('scyther.pokemon.randint')
    def test_same_values(self, mock_rand):
        """Test that odd and even values return either 0 or 15."""
        for i in range(16):
            mock_rand.return_value = i
            if i % 2 == 0:
                expected = 0
            else:
                expected = 15
            self.assertEqual(Pokemon.get_hp_ivs(), expected)

    @parameterized.expand([
        ('all_zero', [4, 2, 0, 14], 0b0000),
        ('one_one', [4, 2, 0, 13], 0b0001),
        ('two_ones', [4, 11, 0, 13], 0b0101),
        ('two_opposite_ones', [9, 8, 7, 6], 0b1010),
        ('three_ones', [15, 7, 7, 6], 0b1110),
        ('all_ones', [1, 3, 5, 7], 0b1111)
    ])
    @mock.patch('scyther.pokemon.randint')
    def test_bit_combination(self, name, rand_vals, expected, mock_rand):
        mock_rand.side_effect = rand_vals
        self.assertEqual(Pokemon.get_hp_ivs(), expected)

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

    @parameterized.expand([
        # Diglett has the lowest base hp
        ("diglett_1_min", 10, 0, 1, 11),
        ("diglett_1_max", 10, 15, 1, 11),
        ("diglett_50_min", 10, 0, 50, 70),
        ("diglett_50_max", 10, 15, 50, 85),
        ("diglett_100_min", 10, 0, 100, 130),
        ("diglett_100_max", 10, 15, 100, 160),
        # Test the mascott
        ("scyther_1_min", 70, 0, 1, 12),
        ("scyther_1_max", 70, 15, 1, 12),
        ("scyther_50_min", 70, 0, 50, 130),
        ("scyther_50_max", 70, 15, 50, 145),
        ("scyther_100_min", 70, 0, 100, 250),
        ("scyther_100_max", 70, 15, 100, 280),
        # Chansey has the highest base hp
        ("chansey_1_min", 250, 0, 1, 16),
        ("chansey_1_max", 250, 15, 1, 16),
        ("chansey_50_min", 250, 0, 50, 310),
        ("chansey_50_max", 250, 15, 50, 325),
        ("chansey_100_min", 250, 0, 100, 610),
        ("chansey_100_max", 250, 15, 100, 640),
    ])
    def test_pokemon_values(self, name, base_hp, hp_ivs, level, expected):
        """Test real world values."""
        self.assertEqual(Pokemon.calculate_hp(base_hp, hp_ivs, level), expected)


class TestInit(TestCase):
    def test_name(self):
        self.assertEqual(Pokemon().name, "Pokemon")
        # Name should just pass through
        self.assertEqual(Pokemon(name="Scyther").name, "Scyther")

    @mock.patch('scyther.pokemon.Pokemon.get_hp_ivs')
    def test_get_hp_ivs(self, mock_ivs):
        """Test that we only call get_hpi_ivs when no hp_ivs are passed in."""
        # Create a new pokemon while passing IVs
        test_pokemon1 = Pokemon(hp_ivs=10)
        self.assertFalse(mock_ivs.called)
        self.assertEqual(test_pokemon1._hp_ivs, 10)

        # Passing no IVs will cause get_hp_ivs to be called
        mock_ivs.return_value = 999
        test_pokemon2 = Pokemon()
        self.assertTrue(mock_ivs.called)
        self.assertEqual(test_pokemon2._hp_ivs, 999)

    @mock.patch('scyther.pokemon.Pokemon.calculate_hp')
    def test_max_hp(self, mock_calc_hp):
        """Max HP should simply be set as the result of calculate_hp."""
        mock_calc_hp.return_value = 99999
        test_pokemon = Pokemon()
        self.assertEqual(test_pokemon.max_hp, 99999)

    def test_status(self):
        # Should default to normal
        test_pokemon1 = Pokemon()
        self.assertEqual(test_pokemon1.status, Status.NORMAL)

        # Should use whatever's passed in
        test_pokemon1 = Pokemon(status="burned")
        self.assertEqual(test_pokemon1.status, Status.BURNED)


class TestCatchBallcheck(TestCase):
    @mock.patch('scyther.pokemon.randint')
    def test_pokeball(self, mock_rand):
        mock_rand.return_value = 35
        test_pokemon = Pokemon(status="burned")
        # This should simply be the random result minus the status effect
        self.assertEqual(test_pokemon._catch_ballcheck(Ball.POKE), 23)
        # Random should be called with the pokeball's range
        mock_rand.assert_called_with(0, 255)
        # A frozen status should lower check value
        test_pokemon.status = Status.FROZEN
        self.assertEqual(test_pokemon._catch_ballcheck(Ball.POKE), 10)

    @mock.patch('scyther.pokemon.randint')
    def test_negative_check(self, mock_rand):
        mock_rand.return_value = 0
        test_pokemon = Pokemon(status="burned")
        # Simply testing that negative values are possible
        self.assertEqual(test_pokemon._catch_ballcheck(Ball.POKE), -12)


class TestCatchHPcheck(TestCase):
    def test_full_hp(self):
        test_pokemon = Pokemon()
        test_pokemon.max_hp = 100
        test_pokemon.current_hp = 100
        self.assertEqual(test_pokemon._catch_hpcheck(Ball.POKE), 85)
        # Great ball is a good test because it performs integer rounding
        self.assertEqual(test_pokemon._catch_hpcheck(Ball.GREAT), 127)

    def test_low_hp(self):
        # Low hp values should be higher than the high hp values
        test_pokemon = Pokemon()
        test_pokemon.max_hp = 10
        test_pokemon.current_hp = 2
        self.assertEqual(test_pokemon._catch_hpcheck(Ball.POKE), 212)
        self.assertEqual(test_pokemon._catch_hpcheck(Ball.GREAT), 255)


class TestCatch(TestCase):
    def test_ghost_marowak(self):
        """Ghost marowak is uncatchable."""
        test_pokemon = Pokemon(is_ghost_marowak=True)
        self.assertFalse(test_pokemon.catch(Ball.MASTER))

    def test_masterball(self):
        """Masterballs always catch."""
        self.assertTrue(Pokemon().catch(Ball.MASTER))

    @mock.patch('scyther.pokemon.Pokemon._catch_ballcheck')
    def test_negative_ballcheck(self, ballcheck):
        """A negative ballcheck higher will always catch."""
        ballcheck.return_value = -10
        self.assertTrue(Pokemon().catch(Ball.POKE))

    @mock.patch('scyther.pokemon.Pokemon._catch_ballcheck')
    def test_ballcheck_catchrate(self, ballcheck):
        """A ballcheck higher than the pokemon's catchrate will always fail."""
        ballcheck.return_value = 70
        self.assertFalse(Pokemon(catch_rate=35).catch(Ball.POKE))

    @mock.patch('scyther.pokemon.randint')
    @mock.patch('scyther.pokemon.Pokemon._catch_hpcheck')
    @mock.patch('scyther.pokemon.Pokemon._catch_ballcheck')
    def test_hpcheck(self, ballcheck, hpcheck, mock_rand):
        """An HP check greater than the random value wil catch."""
        ballcheck.return_value = 10
        hpcheck.return_value = 75
        mock_rand.return_value = 70
        self.assertTrue(Pokemon(catch_rate=35).catch(Ball.POKE))
        # Equal values should catch
        hpcheck.return_value = 70
        self.assertTrue(Pokemon(catch_rate=35).catch(Ball.POKE))

    @mock.patch('scyther.pokemon.randint')
    @mock.patch('scyther.pokemon.Pokemon._catch_hpcheck')
    @mock.patch('scyther.pokemon.Pokemon._catch_ballcheck')
    def test_fail_all(self, ballcheck, hpcheck, mock_rand):
        """When all checks fail, catching will fail."""
        ballcheck.return_value = 10
        hpcheck.return_value = 75
        mock_rand.return_value = 80
        self.assertFalse(Pokemon(catch_rate=35).catch(Ball.POKE))


class TestAnimate(TestCase):
    @parameterized.expand([
        ('impossible', [256, 999], 3, ""),  # Should never actually happen
        ("no_wobbles", [-10, 0, 9], 0, "The ball missed the POKEéMON!"),
        ("one_wobble", [10, 20, 29], 1, "Darn! The POKEéMON broke free!"),
        ("two_wobble", [30, 55, 69], 2, "Aww! It appeared to be caught!"),
        ("three_wobble", [70, 150, 255], 3, "Shoot! It was close too!"),
    ])
    @mock.patch('scyther.ball.Ball')
    def test_each_wobble(self, name, catch_rates, expected_wobbles, expected_msg, mock_ball):
        mock_ball.Ultra.catch_modifier = 100
        for catch_rate in catch_rates:
            pokemon = Pokemon(catch_rate=catch_rate)
            wobbles, msg = pokemon.animate(mock_ball.Ultra)
            self.assertEqual(wobbles, expected_wobbles)
            self.assertEqual(msg, expected_msg)
