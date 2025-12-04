from dataclasses import dataclass
from typing import Dict
from params import GameParams
from players import DCStrategy, ADVStrategy

# 2x2 normal form game for CAG (Hide-and-Seek)
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
    probProtectSuccess = params.q_P(p)
    dcBenefitP = params.B_priv_P(p)
    dcCostP = params.C_P(p)

    # row 0: DC = protect (P)
    # (P, E)
    dcPE = dcBenefitP - dcCostP - params.L * probProtectSuccess
    advPE = params.V * probProtectSuccess - params.C_E

    # (P, T)
    dcPT = dcBenefitP - dcCostP
    advPT = 0.0

    # row 1: DC = transparent (T)
    # (T, E)
    dcTE = params.B_priv_T - params.C_T - params.L * params.q_T
    advTE = params.V * params.q_T - params.C_E

    # (T, T)
    dcTT = params.B_priv_T - params.C_T
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

def compute_mixed_equilibrium(matrix):
    # extract DC payoffs
    a = matrix.dc[0][0]   # (P, E)
    b = matrix.dc[0][1]   # (P, T)
    c = matrix.dc[1][0]   # (T, E)
    d = matrix.dc[1][1]   # (T, T)

    # extract ADV payoffs
    e = matrix.adv[0][0]  # (P, E)
    f = matrix.adv[0][1]  # (P, T)
    g = matrix.adv[1][0]  # (T, E)
    h = matrix.adv[1][1]  # (T, T)

    # solve for x* (prob DC plays P)
    # ADV indifferent:
    denomAdv = (e - g) - (f - h)
    if abs(denomAdv) < 1e-12:
        raise ValueError("No interior mixed NE: ADV indifference denom = 0")

    xStar = (h - g) / denomAdv
    # solve for y* (prob ADV plays E)
    # DC indifferent:
    # y*(a - c) + (1 - y)*(b - d) = 0
    denomDc = (a - c) - (b - d)
    if abs(denomDc) < 1e-12:
        raise ValueError("No interior mixed NE: DC indifference denom = 0")

    yStar = (d - b) / denomDc

    # interior mixed NE must have probabilities in [0,1]
    if not (0.0 <= xStar <= 1.0 and 0.0 <= yStar <= 1.0):
        raise ValueError(f"No interior mixed NE: got x*={xStar}, y*={yStar}")

    return xStar, yStar

def equilibrium_metrics_from_mixed(p, params, dcMatrix, advMatrix, xStar, yStar):
    """
    Given:
      - aggregation threshold p
      - model parameters
      - a 2x2 payoff matrix for (DC, ADV)
      - an interior mixed equilibrium (x*, y*)

    compute:
      - leakage probability
      - expected DC payoff
      - expected ADV payoff

    and return them (plus p, x*, y*) as a dict.
    """
    x = xStar   # prob DC plays P (row 0)
    y = yStar   # prob ADV plays E (col 0)

    # Effective success probability of an attack under DC's mixed strategy
    qP = params.q_P(p)
    q_eff = x * qP + (1.0 - x) * params.q_T

    # Expected probability of successful deanonymization
    leakage_prob = y * q_eff

    # Probabilities of each action profile at equilibrium
    prob_PE = x * y               # (P, E)
    prob_PT = x * (1.0 - y)       # (P, T)
    prob_TE = (1.0 - x) * y       # (T, E)
    prob_TT = (1.0 - x) * (1.0 - y)  # (T, T)

    # Expected payoffs at equilibrium
    dc_payoff = (
        prob_PE * dcMatrix[0][0] +
        prob_PT * dcMatrix[0][1] +
        prob_TE * dcMatrix[1][0] +
        prob_TT * dcMatrix[1][1]
    )
    adv_payoff = (
        prob_PE * advMatrix[0][0] +
        prob_PT * advMatrix[0][1] +
        prob_TE * advMatrix[1][0] +
        prob_TT * advMatrix[1][1]
    )

    return {
        "p": p,
        "x_star": x,
        "y_star": y,
        "leakage_prob": leakage_prob,
        "dc_payoff": dc_payoff,
        "adv_payoff": adv_payoff,
    }

# def equilibrium_metrics(p: int, params: GameParams) -> dict:
#     """
#     Convenience function:
#       - builds the game for p
#       - computes the mixed NE
#       - computes expected leakage + expected payoffs at equilibrium

#     Returns a dict so simulate.py can easily sweep and tabulate.
#     """
#     dcMatrix, advMatrix = build_cag_payoff_matrix(p, params)
#     xStar, yStar = compute_mixed_equilibrium(dcMatrix, advMatrix)

#     x = xStar
#     y = yStar

#     # Effective success probability given DC's mix
#     qP = params.q_P(p)
#     q_eff = x * qP + (1.0 - x) * params.q_T

#     # Expected probability of successful deanonymization
#     leakage_prob = y * q_eff

#     # Expected payoffs for each player at equilibrium
#     # Enumerate profiles: (P,E), (P,T), (T,E), (T,T)
#     prob_PE = x * y
#     prob_PT = x * (1.0 - y)
#     prob_TE = (1.0 - x) * y
#     prob_TT = (1.0 - x) * (1.0 - y)

#     dc_payoff = (
#         prob_PE * matrix.dc[0][0] +
#         prob_PT * matrix.dc[0][1] +
#         prob_TE * matrix.dc[1][0] +
#         prob_TT * matrix.dc[1][1]
#     )
#     adv_payoff = (
#         prob_PE * matrix.adv[0][0] +
#         prob_PT * matrix.adv[0][1] +
#         prob_TE * matrix.adv[1][0] +
#         prob_TT * matrix.adv[1][1]
#     )

#     return {
#         "p": p,
#         "x_star": x,
#         "y_star": y,
#         "leakage_prob": leakage_prob,
#         "dc_payoff": dc_payoff,
#         "adv_payoff": adv_payoff,
#     }
