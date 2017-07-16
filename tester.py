#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple end-to-end tester with some convience methods.

Note:
    Basically just an ipdb shell kicked off with imports and predifed functions.
"""

import time

import ipdb

from scyther.ball import Ball
from scyther.pokemon import Pokemon
from scyther.status import Status

# Create a scyther to play around with
SCYTHER = Pokemon(
    base_hp=70,
    hp_ivs=None,
    level=25,
    catch_rate=45,
    status="normal",
    name="Scyther",
    is_ghost_marowak=False
)


def emulate(ball=Ball.poke):
    if SCYTHER.catch(ball):
        wobbles = 4
        message = "{} Caught successfully!".format(SCYTHER.name)
    else:
        wobbles, message = SCYTHER.animate(ball)

    for wobble in range(wobbles):
        print("Wobble...")
        time.sleep(0.2)

    print(message)


if __name__ == '__main__':
    ipdb.set_trace()
