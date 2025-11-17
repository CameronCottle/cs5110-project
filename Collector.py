#File containing the functions for the data collecter class

# Collector.py
from __future__ import annotations
from typing import Any, Dict, List, Optional, Sequence
import random

from Player import Player


class DataCollector(Player):
    """
    DataCollector: normal-form game agent for Owner–Collector (OCG) or
    Collector–Adversary (CAG) interactions, modeled like DataOwner.

    Actions default to ["C", "D"]:
      - In OCG (owner vs collector): "C" can mean offer/increase incentive or
        higher-quality service (more cost to collector), "D" means do nothing.
      - In CAG (collector vs adversary): "C" can mean aggregate/protect (e.g., p-destination),
        "D" means abstain (lower cost, lower protection).

    Policies:
      - "fixed_mixed": sample from self.mixed_strategy
      - "best_response": argmax expected payoff vs opponent_mixed
      - "fictitious_play": best-respond to learned opponent frequencies
      - "epsilon_greedy": explore with epsilon, else best_response

    Notes:
      * Payoffs are supplied by `main.py` as a matrix, same convention as Owner:
        my_payoffs[i][j] is THIS collector's payoff when I play actions[i]
        against opponent action opp_actions[j].
      * Collector-specific knobs (incentive, price, budget, epsilon_privacy)
        are provided as lightweight state you can use when constructing the
        payoff matrix in `main.py`.
    """

    def __init__(
        self,
        name: str = "",
        actions: Optional[List[str]] = None,
        policy: str = "best_response",
        mixed_strategy: Optional[Dict[str, float]] = None,
        epsilon: float = 0.05,
        seed: Optional[int] = None,
        # Collector-specific knobs you can use when building payoffs:
        incentive_level: float = 0.0,     # how much incentive (cash/utility) offered to owners
        price_per_query: float = 0.0,     # revenue per served request/query
        budget: float = float("inf"),     # available budget for incentives/defense
        epsilon_privacy: float = None,    # DP/LDP epsilon, if you model it
    ) -> None:
        super().__init__(name=name)
        self.actions: List[str] = actions or ["C", "D"]
        self.policy = policy
        self.epsilon = float(epsilon)
        self._rng = random.Random(seed)

        # Opponent belief state (for fictitious play)
        self._opp_actions: List[str] = []
        self._opp_counts: Dict[str, int] = {}
        self._opp_probs: Dict[str, float] = {}

        # Mixed strategy (used if policy == "fixed_mixed")
        if mixed_strategy is None:
            mixed_strategy = {a: 1.0 / len(self.actions) for a in self.actions}
        self.mixed_strategy = self._normalize_dist(mixed_strategy, self.actions)

        # Collector-specific economic/privacy knobs (for payoff construction)
        self.incentive_level = float(incentive_level)
        self.price_per_query = float(price_per_query)
        self.budget = float(budget)
        self.epsilon_privacy = epsilon_privacy

        # Bookkeeping (optional)
        self.total_spend = 0.0
        self.total_revenue = 0.0

    # --- Abstract interface impl ---
    def defect(self) -> Any:
        return "D" if "D" in self.actions else self.actions[-1]

    def cooperate(self) -> Any:
        return "C" if "C" in self.actions else self.actions[0]

    # --- Main decision function ---
    def choose_action(
        self,
        my_payoffs: Sequence[Sequence[float]],
        opp_actions: Optional[List[str]] = None,
        opponent_mixed: Optional[Dict[str, float]] = None,
    ) -> str:
        """
        Pick an action according to self.policy.

        Args:
          my_payoffs: matrix (len(self.actions) x len(opp_actions));
                      my_payoffs[i][j] is THIS collector's payoff when I play actions[i]
                      vs opp_actions[j]
          opp_actions: labels for opponent actions (columns of my_payoffs)
          opponent_mixed: dist over opp_actions; required for best_response / epsilon_greedy.
                          If None, defaults to uniform or learned frequencies.
        """
        opp_actions = opp_actions or (["C", "D"] if len(self.actions) == 2 else None)
        if opp_actions is None:
            raise ValueError("opp_actions must be provided when actions are not ['C','D'].")

        # Initialize belief support once
        if not self._opp_actions:
            self._opp_actions = list(opp_actions)
            self._opp_counts = {a: 0 for a in self._opp_actions}
            self._opp_probs = {a: 1.0 / len(self._opp_actions) for a in self._opp_actions}

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
        Update internal beliefs after a round (used by fictitious play).
        Also a good place to update budget/spend if you're modeling that.
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

        # Optional: book-keeping (you can wire these from main if desired)
        # e.g., positive payoff could be revenue; negative could be cost/spend.
        if my_payoff >= 0:
            self.total_revenue += my_payoff
        else:
            self.total_spend += -my_payoff

    # --- Collector knobs (optional helpers) ---
    def set_incentive(self, value: float) -> None:
        self.incentive_level = float(value)

    def set_price(self, value: float) -> None:
        self.price_per_query = float(value)

    def set_budget(self, value: float) -> None:
        self.budget = float(value)

    def set_privacy_epsilon(self, value: Optional[float]) -> None:
        self.epsilon_privacy = value

    def set_mixed_strategy(self, probs: Dict[str, float]) -> None:
        self.mixed_strategy = self._normalize_dist(probs, self.actions)

    # --- Internals ---
    def _best_response(
        self,
        my_payoffs: Sequence[Sequence[float]],
        opp_actions: List[str],
        opp_dist: Dict[str, float],
    ) -> str:
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
        x = self._rng.random()
        cum = 0.0
        for a in self.actions:
            cum += dist.get(a, 0.0)
            if x <= cum:
                return a
        return self.actions[-1]

    @staticmethod
    def _normalize_dist(dist: Dict[str, float], support: List[str]) -> Dict[str, float]:
        clipped = {a: max(0.0, float(dist.get(a, 0.0))) for a in support}
        s = sum(clipped.values())
        if s <= 0.0:
            return {a: 1.0 / len(support) for a in support}
        return {a: v / s for a, v in clipped.items()}
