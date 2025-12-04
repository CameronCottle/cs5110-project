from dataclasses import dataclass
from math import exp

# constains all economic / privacy parameters for the CAG (Hide-and-Seek) game.

@dataclass
class GameParams:
    # adversary parameters
    advValueSuccess: float
    advAttackCost: float
    successProbTransparent: float

    # data collector privacy loss
    dcLossOnBreach: float

    # data collector baseline utility under T
    dcPrivacyBenefitTransparent: float
    dcCostTransparent: float

    # coefficients controlling how protection P behaves as p increases
    alpha: float
    beta: float
    gamma: float

    # functional forms in p

    # probability adversary succeeds when DC protects with threshold p.
    def successProbProtected(self, p):
        return self.successProbTransparent * exp(-self.alpha * p)

    # privacy benefit to DC when it plays P at threshold p.

    def dcPrivacyBenefitProtected(self, p):
        return self.dcPrivacyBenefitTransparent + self.beta * p

    # query processing cost for DC when it plays P at threshold p.
    def dcCostProtected(self, p):
        return self.dcCostTransparent + self.gamma * p


def default_params() -> GameParams:
    return GameParams(
        advValueSuccess=10.0,
        advAttackCost=6.0,
        successProbTransparent=0.7,
        dcLossOnBreach=8.0,
        dcPrivacyBenefitTransparent=1.0,
        dcCostTransparent=1.0,
        alpha=0.25,
        beta=0.1,
        gamma=0.5,
    )
