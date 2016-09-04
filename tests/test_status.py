# -*- coding: utf-8 -*-
"""Tests for Status."""

from unittest import TestCase

from scyther.pokemon import Status


class TestStatusNames(TestCase):
    def test_names(self):
        names = Status.names()
        self.assertListEqual(names, ['normal', 'poisoned',
                                     'burned', 'paralyzed',
                                     'asleep', 'frozen'])
