# players.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import random

DCStrategy = Literal["P", "T"]   # Protect / Transparent
ADVStrategy = Literal["E", "T"]  # Exploit / Tolerate


@dataclass
class DataCollector:
    """
    Data collector (trusted third party) in the CAG.
    For analytic work, you mostly care about its mixed strategy x (probability of P).
    For simulations, use `choose_action`.
    """
    name: str = "DataCollector"

    def choose_action(self, x: float) -> DCStrategy:
        """
        Sample an action according to mixed strategy x:
          P with probability x, T with probability 1-x.
        """
        r = random.random()
        return "P" if r < x else "T"


@dataclass
class Adversary:
    """
    Adversary who may try to track a target user.
    Uses mixed strategy y (probability of E).
    """
    name: str = "Adversary"

    def choose_action(self, y: float) -> ADVStrategy:
        """
        Sample an action according to mixed strategy y:
          E with probability y, T with probability 1-y.
        """
        r = random.random()
        return "E" if r < y else "T"
