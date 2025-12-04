from dataclasses import dataclass
from typing import Dict
from params import GameParams
from players import DCStrategy, ADVStrategy

# 2x2 normal form game for CAG (hide-and-seek)
@dataclass
class PayoffMatrix2x2:
    dc: list[list[float]]
    adv: list[list[float]]

    def payoff(self, dcAction: DCStrategy, advAction: ADVStrategy):
        row = 0 if dcAction == "P" else 1
        col = 0 if advAction == "E" else 1
        return self.dc[row][col], self.adv[row][col]

# mixed-strategy Nash equilibrium for 2x2 game
@dataclass
class MixedEquilibrium2x2:
    xStar: float
    yStar: float

# build the payoff matrix
def build_payoff_matrix(p, params):
    # values that depend on p
    probProtectSuccess = params.successProbProtected(p)
    dcBenefitP = params.dcPrivacyBenefitProtected(p)
    dcCostP = params.dcCostProtected(p)

    # row 0: DC = protect (P)
    # (P, E)
    dcPE = dcBenefitP - dcCostP - params.dcLossOnBreach * probProtectSuccess
    advPE = params.advValueSuccess * probProtectSuccess - params.advAttackCost

    # (P, T)
    dcPT = dcBenefitP - dcCostP
    advPT = 0.0

    # row 1: DC = transparent (T)
    # (T, E)
    dcTE = (params.dcPrivacyBenefitTransparent - params.dcCostTransparent - params.dcLossOnBreach * params.successProbTransparent)
    advTE = (params.advValueSuccess * params.successProbTransparent - params.advAttackCost)

    # (T, T)
    dcTT = params.dcPrivacyBenefitTransparent - params.dcCostTransparent
    advTT = 0.0

    # create matrices
    dcMatrix = [
        [dcPE, dcPT],
        [dcTE, dcTT],
    ]

    advMatrix = [
        [advPE, advPT],
        [advTE, advTT],
    ]

    return dcMatrix, advMatrix


# compute mixed-strategy Nash equilibrium for 2x2 game
def compute_mixed_equilibrium(dcMatrix, advMatrix):
    # extract DC payoffs
    a = dcMatrix[0][0]   # (P, E)
    b = dcMatrix[0][1]   # (P, T)
    c = dcMatrix[1][0]   # (T, E)
    d = dcMatrix[1][1]   # (T, T)

    # extract ADV payoffs
    e = advMatrix[0][0]  # (P, E)
    f = advMatrix[0][1]  # (P, T)
    g = advMatrix[1][0]  # (T, E)
    h = advMatrix[1][1]  # (T, T)

    # solve for x* (prob DC plays P)
    denomAdv = (e - g) - (f - h)
    if abs(denomAdv) < 1e-12:
        raise ValueError("No interior mixed NE: ADV indifference denom = 0")
    xStar = (h - g) / denomAdv

    # solve for y* (prob ADV plays E)
    denomDc = (a - c) - (b - d)
    if abs(denomDc) < 1e-12:
        raise ValueError("No interior mixed NE: DC indifference denom = 0")
    yStar = (d - b) / denomDc

    # interior mixed NE must have probabilities in [0,1]
    if not (0.0 <= xStar <= 1.0 and 0.0 <= yStar <= 1.0):
        raise ValueError(f"No interior mixed NE: got x*={xStar}, y*={yStar}")

    return xStar, yStar

# compute expected leakage and payoffs at mixed NE
def equilibrium_metrics_from_mixed(p, params, dcMatrix, advMatrix, xStar, yStar):
    x = xStar   # prob DC plays P (row 0)
    y = yStar   # prob ADV plays E (col 0)

    # Effective success probability of an attack under DC's mixed strategy
    qP = params.successProbProtected(p)
    qEff = x * qP + (1.0 - x) * params.successProbTransparent

    # Expected probability of successful deanonymization
    leakageProb = y * qEff

    # Probabilities of each action profile at equilibrium
    probPE = x * y
    probPT = x * (1.0 - y)
    probTE = (1.0 - x) * y
    probTT = (1.0 - x) * (1.0 - y)

    # Expected payoffs at equilibrium
    dcPayoff = (probPE * dcMatrix[0][0] + probPT * dcMatrix[0][1] + probTE * dcMatrix[1][0] + probTT * dcMatrix[1][1])
    advPayoff = (probPE * advMatrix[0][0] + probPT * advMatrix[0][1] + probTE * advMatrix[1][0] + probTT * advMatrix[1][1])

    return {
        "p": p,
        "x_star": x,
        "y_star": y,
        "leakage_prob": leakageProb,
        "dc_payoff": dcPayoff,
        "adv_payoff": advPayoff,
    }
