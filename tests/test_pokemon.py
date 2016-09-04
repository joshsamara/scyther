# -*- coding: utf-8 -*-
"""Tests for Pokemon class."""

from scyther.pokemon import Pokemon

from nose.tools import nottest


#TODO:
@nottest
def test_get_hp_ivs():
    assert Pokemon.get_hp_ivs() == 0
