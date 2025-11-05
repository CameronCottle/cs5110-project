#File defining the data owner class and all their functions

from __future__ import annotations
from typing import Any, Dict, List, Optional, Sequence
import random

from Player import Player


class DataOwner(Player):
    """
    Normal-form game agent for Owner–Owner (OOG) style games.

    Actions: defaults to ["C", "D"] but any labels are supported.
    Policies:
      - "fixed_mixed": sample from self.mixed_strategy
      - "best_response": argmax expected payoff vs opponent_mixed
      - "fictitious_play": best-respond to learned opponent frequencies
      - "epsilon_greedy": explore with epsilon, else best_response
    """

    def __init__(
        self,
        name: str = "",
        actions: Optional[List[str]] = None,
        policy: str = "best_response",
        mixed_strategy: Optional[Dict[str, float]] = None,
        epsilon: float = 0.05,
        seed: Optional[int] = None,
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
          my_payoffs: matrix with shape (len(self.actions), len(opp_actions));
                      my_payoffs[i][j] is my payoff when I play actions[i] vs opp_actions[j]
          opp_actions: list of opponent action labels (order = columns of my_payoffs)
          opponent_mixed: distribution over opp_actions; needed for best_response/epsilon_greedy.
                          If None, defaults to uniform or learned frequencies (fictitious_play).

        Returns:
          action label from self.actions
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
            # fall through to best response with available distribution
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
        """
        if opp_action not in self._opp_counts:
            # add unseen action label
            self._opp_actions.append(opp_action)
            self._opp_counts[opp_action] = 0
            # expand probs uniformly and renormalize
            for a in self._opp_actions:
                self._opp_probs[a] = 1.0 / len(self._opp_actions)

        self._opp_counts[opp_action] += 1
        total = sum(self._opp_counts.values())
        if total > 0:
            for a in self._opp_actions:
                self._opp_probs[a] = self._opp_counts[a] / total

    def set_mixed_strategy(self, probs: Dict[str, float]) -> None:
        """Set a fixed mixed strategy (for policy='fixed_mixed')."""
        self.mixed_strategy = self._normalize_dist(probs, self.actions)

    # --- Helpers ---
    def _best_response(
        self,
        my_payoffs: Sequence[Sequence[float]],
        opp_actions: List[str],
        opp_dist: Dict[str, float],
    ) -> str:
        # map opponent action -> column index
        col_index = {a: j for j, a in enumerate(opp_actions)}

        # compute expected payoff per my action
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

        # break ties randomly
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
