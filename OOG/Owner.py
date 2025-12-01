# Owner.py
from __future__ import annotations
from typing import Any, Dict, List, Optional, Sequence
import random

from Player import Player


class DataOwner(Player):
    """
    Data owner in the pseudonym change game (Freudiger et al.).

    self.u is the current payoff (location-privacy utility minus costs)
    just BEFORE the next game. Each game updates self.u to the new payoff.
    """

    def __init__(
        self,
        name: str = "",
        actions: Optional[List[str]] = None,
        policy: str = "best_response",
        mixed_strategy: Optional[Dict[str, float]] = None,
        epsilon: float = 0.05,
        seed: Optional[int] = None,
        # Freudiger-model parameters:
        gamma: float = 0.2,          # cost of changing pseudonym (γ)
        lambda_loss: float = 0.05,   # privacy loss rate (λ) per time step
        initial_privacy: float = 1.0,  # initial location-privacy value A_i
        threshold: Optional[float] = None,  # for policy='threshold'
    ) -> None:
        super().__init__(name=name)
        self.actions: List[str] = actions or ["C", "D"]
        self.policy = policy
        self.epsilon = float(epsilon)
        self._rng = random.Random(seed)

        # Opponent beliefs (for fictitious_play)
        self._opp_actions: List[str] = []
        self._opp_counts: Dict[str, int] = {}
        self._opp_probs: Dict[str, float] = {}

        # Mixed strategy for fixed_mixed
        if mixed_strategy is None:
            mixed_strategy = {a: 1.0 / len(self.actions) for a in self.actions}
        self.mixed_strategy = self._normalize_dist(mixed_strategy, self.actions)

        # Freudiger parameters
        self.gamma = float(gamma)
        self.lambda_loss = float(lambda_loss)
        # Start with payoff u = initial_privacy - gamma (as if we just did a
        # successful change with cost γ)
        self.u: float = float(initial_privacy) - self.gamma
        self.threshold: Optional[float] = threshold  # θ̃ for threshold policy

        # Optional bookkeeping
        self.total_score: float = 0.0  # if you still want a cumulative score

    # --- Abstract interface impl ---
    def defect(self) -> Any:
        return "D" if "D" in self.actions else self.actions[-1]

    def cooperate(self) -> Any:
        return "C" if "C" in self.actions else self.actions[0]

    # --- Freudiger-style privacy loss between games ---
    def apply_privacy_loss(self, dt: float = 1.0) -> None:
        """
        Approximate the user-centric privacy loss β_i(t) = λ (t - T_i^ℓ).
        Here we model it simply as linear decay of u at rate lambda_loss.
        (u is always kept non-negative.)
        """
        self.u = max(0.0, self.u - self.lambda_loss * dt)

    # --- Main decision function ---
    def choose_action(
        self,
        my_payoffs: Sequence[Sequence[float]],
        opp_actions: Optional[List[str]] = None,
        opponent_mixed: Optional[Dict[str, float]] = None,
    ) -> str:
        opp_actions = opp_actions or (["C", "D"] if len(self.actions) == 2 else None)
        if opp_actions is None:
            raise ValueError("opp_actions must be provided when actions are not ['C','D'].")

        # initialize opponent belief support
        if not self._opp_actions:
            self._opp_actions = list(opp_actions)
            self._opp_counts = {a: 0 for a in self._opp_actions}
            self._opp_probs = {a: 1.0 / len(self._opp_actions) for a in self._opp_actions}

        # New: threshold policy (I-game style)
        if self.policy == "threshold":
            if self.threshold is None:
                raise ValueError("threshold policy requires self.threshold to be set.")
            # θ_i is the current payoff just before the game (u^- in the paper)
            theta_i = self.u
            return "C" if theta_i <= self.threshold else "D"

        if self.policy == "fixed_mixed":
            return self._sample_from(self.mixed_strategy)

        if self.policy == "fictitious_play":
            dist = self._opp_probs if any(self._opp_counts.values()) else {
                a: 1.0 / len(opp_actions) for a in opp_actions
            }
            return self._best_response(my_payoffs, opp_actions, dist)

        if self.policy == "epsilon_greedy":
            if self._rng.random() < self.epsilon:
                return self._rng.choice(self.actions)
            dist = (opponent_mixed or
                    (self._opp_probs if any(self._opp_counts.values()) else {
                        a: 1.0 / len(opp_actions) for a in opp_actions
                    }))
            dist = self._normalize_dist(dist, opp_actions)
            return self._best_response(my_payoffs, opp_actions, dist)

        if self.policy == "best_response":
            dist = opponent_mixed or {a: 1.0 / len(opp_actions) for a in opp_actions}
            dist = self._normalize_dist(dist, opp_actions)
            return self._best_response(my_payoffs, opp_actions, dist)

        raise ValueError(f"Unknown policy '{self.policy}'")

    def observe_outcome(self, my_action: str, opp_action: str, my_payoff: float) -> None:
        """
        Update beliefs as before, and also update self.u to the new payoff
        (this matches the paper where u_i becomes u_i^- before the next game).
        """
        if opp_action not in self._opp_counts:
            self._opp_actions.append(opp_action)
            self._opp_counts[opp_action] = 0
            for a in self._opp_actions:
                self._opp_probs[a] = 1.0 / len(self._opp_actions)

        self._opp_counts[opp_action] += 1
        total = sum(self._opp_counts.values())
        if total > 0:
            for a in self._opp_actions:
                self._opp_probs[a] = self._opp_counts[a] / total

        self.u = float(my_payoff)
        self.total_score += my_payoff

    # --- INTERNAL HELPERS ---

    def _best_response(
        self,
        my_payoffs: Sequence[Sequence[float]],
        opp_actions: List[str],
        opp_dist: Dict[str, float],
    ) -> str:
        """
        Compute best response to opponent mixed strategy.
        """
        col_index = {a: j for j, a in enumerate(opp_actions)}

        best_val = None
        best_actions: List[str] = []

        for i, my_act in enumerate(self.actions):
            expected = 0.0
            for a, p in opp_dist.items():
                j = col_index[a]
                expected += p * float(my_payoffs[i][j])

            if best_val is None or expected > best_val:
                best_val = expected
                best_actions = [my_act]
            elif expected == best_val:
                best_actions.append(my_act)

        return self._rng.choice(best_actions)

    def _sample_from(self, dist: Dict[str, float]) -> str:
        """
        Sample an action from a probability distribution.
        """
        x = self._rng.random()
        cum = 0.0
        for a in self.actions:
            cum += dist.get(a, 0.0)
            if x <= cum:
                return a
        return self.actions[-1]

    @staticmethod
    def _normalize_dist(dist: Dict[str, float], support: List[str]) -> Dict[str, float]:
        """
        Ensure probabilities sum to 1 and only include valid support actions.
        """
        clipped = {a: max(0.0, float(dist.get(a, 0.0))) for a in support}
        s = sum(clipped.values())
        if s <= 0.0:
            return {a: 1.0 / len(support) for a in support}
        return {a: v / s for a, v in clipped.items()}

