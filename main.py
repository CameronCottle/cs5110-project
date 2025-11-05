# main.py
from Owner import DataOwner

# Example payoff matrix for Player 1 (rows=C,D vs cols=C,D)
# You can adjust these numbers or later compute them dynamically from A, δ, β, α
p1_payoffs = [
    [8.0, 2.0],  # P1 plays C vs (C,D)
    [6.0, 0.0],  # P1 plays D vs (C,D)
]

# Player 2's payoffs (mirror or asymmetric version)
p2_payoffs = [
    [8.0, 6.0],  # P2 plays C vs (C,D)
    [2.0, 0.0],  # P2 plays D vs (C,D)
]

opp_actions = ["C", "D"]

# Initialize players
p1 = DataOwner("P1", policy="best_response", seed=1)
p2 = DataOwner("P2", policy="fixed_mixed", mixed_strategy={"C": 0.7, "D": 0.3}, seed=2)

# Initialize score tracking
total_scores = {"P1": 0.0, "P2": 0.0}
num_rounds = 10

# Run repeated game simulation
for t in range(1, num_rounds + 1):
    # Each player chooses an action
    a1 = p1.choose_action(p1_payoffs, opp_actions, opponent_mixed=p2.mixed_strategy)
    a2 = p2.choose_action(p2_payoffs, opp_actions, opponent_mixed={"C": 0.5, "D": 0.5})

    # Determine payoffs from their matrices
    payoff_map_p1 = {
        ("C", "C"): p1_payoffs[0][0],
        ("C", "D"): p1_payoffs[0][1],
        ("D", "C"): p1_payoffs[1][0],
        ("D", "D"): p1_payoffs[1][1],
    }
    payoff_map_p2 = {
        ("C", "C"): p2_payoffs[0][0],
        ("C", "D"): p2_payoffs[0][1],
        ("D", "C"): p2_payoffs[1][0],
        ("D", "D"): p2_payoffs[1][1],
    }

    p1_payoff = payoff_map_p1[(a1, a2)]
    p2_payoff = payoff_map_p2[(a2, a1)]

    # Update cumulative totals
    total_scores["P1"] += p1_payoff
    total_scores["P2"] += p2_payoff

    # Update beliefs for fictitious play or learning policies
    p1.observe_outcome(a1, a2, p1_payoff)
    p2.observe_outcome(a2, a1, p2_payoff)

    # Print round results
    print(f"Round {t:02d}: P1={a1} ({p1_payoff:.1f}) | P2={a2} ({p2_payoff:.1f})")
    print(f"   Running total: P1={total_scores['P1']:.1f}, P2={total_scores['P2']:.1f}")

# Final summary
print("\n=== Final Totals ===")
for name, score in total_scores.items():
    print(f"{name}: {score:.2f}")
