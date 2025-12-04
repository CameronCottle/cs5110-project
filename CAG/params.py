# params.py
from dataclasses import dataclass
from math import exp


@dataclass
class GameParams:
    """
    Encapsulates all economic / privacy parameters for the CAG (Hide-and-Seek) game.
    """

    # Adversary parameters
    V: float        # Value of successful deanonymization
    C_E: float      # Cost of launching an attack
    q_T: float      # Success probability under weak protection (DC plays T)

    # Data collector privacy loss
    L: float        # Loss to DC per successful deanonymization

    # Data collector baseline utility under T
    B_priv_T: float  # Privacy benefit when DC plays T (usually small)
    C_T: float       # Query processing cost when DC plays T

    # Coefficients controlling how protection P behaves as p increases
    alpha: float     # Controls how fast success probability q_P(p) drops
    beta: float      # Controls how fast privacy benefit B_priv_P(p) grows
    gamma: float     # Controls how fast processing cost C_P(p) grows

    # --- Functional forms in p ---

    def q_P(self, p: int) -> float:
        """
        Prob adversary succeeds when DC protects with threshold p.
        Here: q_P(p) = q_T * exp(-alpha * p).
        """
        return self.q_T * exp(-self.alpha * p)

    def B_priv_P(self, p: int) -> float:
        """
        Privacy benefit to DC when it plays P at threshold p.
        Linear in p for simplicity.
        """
        return self.B_priv_T + self.beta * p

    def C_P(self, p: int) -> float:
        """
        Query processing cost for DC when it plays P at threshold p.
        Linear in p for simplicity.
        """
        return self.C_T + self.gamma * p


def default_params() -> GameParams:
    return GameParams(
        V=10.0,
        C_E=6.0,     # attack cost
        q_T=0.7,
        L=8.0,
        B_priv_T=1.0,
        C_T=1.0,
        alpha=0.25,  # how fast q_P(p) drops
        beta=0.1,    # how fast privacy benefit grows
        gamma=0.5,   # how fast P's cost grows
    )
