from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import random

DCStrategy = Literal["P", "T"]   # protect / transparent
ADVStrategy = Literal["E", "T"]  # exploit / tolerate


@dataclass
class DataCollector:
    name: str = "DataCollector"

    def choose_action(self, x):
        r = random.random()
        return "P" if r < x else "T"

@dataclass
class Adversary:
    name: str = "Adversary"

    def choose_action(self, y):
        r = random.random()
        return "E" if r < y else "T"
