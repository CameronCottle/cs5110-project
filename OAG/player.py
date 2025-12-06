from enum import Enum

class OwnerAction(Enum):
    PROTECT = 0
    DEFECT = 1

class AdversaryAction(Enum):
    ATTACK = 0
    ABSTAIN = 1

class Player:
    def __init__(self, name: str):
        self.name = name

class Owner(Player):
    def __init__(self, U, P, C_p, gamma):
        super().__init__("Owner")
        self.U = U
        self.P = P
        self.C_p = C_p
        self.gamma = gamma

class Adversary(Player):
    def __init__(self, G, C_a):
        super().__init__("Adversary")
        self.G = G
        self.C_a = C_a
