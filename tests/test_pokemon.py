# -*- coding: utf-8 -*-
"""Tests for Pokemon class."""

from unittest import TestCase, mock

from scyther.status import Status
from scyther.ball import Ball
from scyther.pokemon import Pokemon


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
        self.assertEqual(Pokemon().name, "Pokemon")
        # Name should just pass through
        self.assertEqual(Pokemon(name="Scyther").name, "Scyther")

    @mock.patch('scyther.pokemon.Pokemon.get_hp_ivs')
    def test_get_hp_ivs(self, mock_ivs):
        """Test that we only call get_hpi_ivs when no hp_ivs are passed in."""
        # Create a new pokemon while passing IVs
        test_pokemon1 = Pokemon( hp_ivs=10)
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
        self.assertEqual(test_pokemon1.status, Status.normal)

        # Should use whatever's passed in
        test_pokemon1 = Pokemon(status="burned")
        self.assertEqual(test_pokemon1.status, Status.burned)


class TestCatchBallcheck(TestCase):
    @mock.patch('scyther.pokemon.randint')
    def test_pokeball(self, mock_rand):
        mock_rand.return_value = 35
        test_pokemon = Pokemon(status="burned")
        # This should simply be the random result minus the status effect
        self.assertEqual(test_pokemon._catch_ballcheck(Ball.poke), 23)
        # Random should be called with the pokeball's range
        mock_rand.assert_called_with(0, 255)
        # A frozen status should lower check value
        test_pokemon.status = Status.frozen
        self.assertEqual(test_pokemon._catch_ballcheck(Ball.poke), 10)

    @mock.patch('scyther.pokemon.randint')
    def test_negative_check(self, mock_rand):
        mock_rand.return_value = 0
        test_pokemon = Pokemon(status="burned")
        # Simply testing that negative values are possible
        self.assertEqual(test_pokemon._catch_ballcheck(Ball.poke), -12)


class TestCatchHPcheck(TestCase):
    def test_full_hp(self):
        test_pokemon = Pokemon()
        test_pokemon.max_hp = 100
        test_pokemon.current_hp = 100
        self.assertEqual(test_pokemon._catch_hpcheck(Ball.poke), 85)
        # Great ball is a good test because it performs integer rounding
        self.assertEqual(test_pokemon._catch_hpcheck(Ball.great), 127)

    def test_low_hp(self):
        # Low hp values should be higher than the high hp values
        test_pokemon = Pokemon()
        test_pokemon.max_hp = 10
        test_pokemon.current_hp = 2
        self.assertEqual(test_pokemon._catch_hpcheck(Ball.poke), 212)
        self.assertEqual(test_pokemon._catch_hpcheck(Ball.great), 255)


class TestCatch(TestCase):
    def test_ghost_marowak(self):
        """Ghost marowak is uncatchable."""
        test_pokemon = Pokemon(is_ghost_marowak=True)
        self.assertFalse(test_pokemon.catch(Ball.master))

    def test_masterball(self):
        """Masterballs always catch."""
        self.assertTrue(Pokemon().catch(Ball.master))

    @mock.patch('scyther.pokemon.Pokemon._catch_ballcheck')
    def test_negative_ballcheck(self, ballcheck):
        """A negative ballcheck higher will always catch."""
        ballcheck.return_value = -10
        self.assertTrue(Pokemon().catch(Ball.poke))

    @mock.patch('scyther.pokemon.Pokemon._catch_ballcheck')
    def test_ballcheck_catchrate(self, ballcheck):
        """A ballcheck higher than the pokemon's catchrate will always fail."""
        ballcheck.return_value = 70
        self.assertFalse(Pokemon(catch_rate=35).catch(Ball.poke))

    @mock.patch('scyther.pokemon.randint')
    @mock.patch('scyther.pokemon.Pokemon._catch_hpcheck')
    @mock.patch('scyther.pokemon.Pokemon._catch_ballcheck')
    def test_hpcheck(self, ballcheck, hpcheck, mock_rand):
        """An HP check greater than the random value wil catch."""
        ballcheck.return_value = 10
        hpcheck.return_value = 75
        mock_rand.return_value = 70
        self.assertTrue(Pokemon(catch_rate=35).catch(Ball.poke))
        # Equal values should catch
        hpcheck.return_value = 70
        self.assertTrue(Pokemon(catch_rate=35).catch(Ball.poke))

    @mock.patch('scyther.pokemon.randint')
    @mock.patch('scyther.pokemon.Pokemon._catch_hpcheck')
    @mock.patch('scyther.pokemon.Pokemon._catch_ballcheck')
    def test_fail_all(self, ballcheck, hpcheck, mock_rand):
        """When all checks fail, catching will fail."""
        ballcheck.return_value = 10
        hpcheck.return_value = 75
        mock_rand.return_value = 80
        self.assertFalse(Pokemon(catch_rate=35).catch(Ball.poke))


class TestAnimate(TestCase):
    def test_impossible(self):
        pokemon = Pokemon(catch_rate=999)
        wobbles, msg = pokemon.animate(Ball.ultra)
        self.assertEqual(wobbles, 3)
        self.assertEqual(msg, "")

    @mock.patch('scyther.ball.Ball')
    def test_impossible_edge(self, mock_ball):
        """Test where where the animation check is exactly 255."""
        pokemon = Pokemon(catch_rate=255)
        mock_ball.catch_modifier = mock.PropertyMock(return_value=100)
        wobbles, msg = pokemon.animate(Ball.ultra)
        self.assertEqual(wobbles, 3)
        self.assertEqual(msg, "Shoot! It was close too!")

    # TODO: Parameterize these tests
    @mock.patch('scyther.ball.Ball')
    def test_less_than_10(self, mock_ball):
        pokemon = Pokemon(catch_rate=9)
        mock_ball.catch_modifier = mock.PropertyMock(return_value=100)
        wobbles, msg = pokemon.animate(Ball.ultra)
        self.assertEqual(wobbles, 0)
        self.assertEqual(msg, "The ball missed the POKEéMON!")

    @mock.patch('scyther.ball.Ball')
    def test_less_than_30(self, mock_ball):
        pokemon = Pokemon(catch_rate=22)
        mock_ball.catch_modifier = mock.PropertyMock(return_value=100)
        wobbles, msg = pokemon.animate(Ball.ultra)
        self.assertEqual(wobbles, 1)
        self.assertEqual(msg, "Darn! The POKEéMON broke free!")

    @mock.patch('scyther.ball.Ball')
    def test_less_than_70(self, mock_ball):
        pokemon = Pokemon(catch_rate=55)
        mock_ball.catch_modifier = mock.PropertyMock(return_value=100)
        wobbles, msg = pokemon.animate(Ball.ultra)
        self.assertEqual(wobbles, 2)
        self.assertEqual(msg, "Aww! It appeared to be caught!")
