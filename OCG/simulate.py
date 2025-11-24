from typing import Dict, List
from players import TaxiService, generate_random_passengers
from mechanisms import vcg_winner, exponential_dp_winner

# returns a dictionary with the results of a single world simulation
def run_single_world(num_passengers, epsilon):
    game = TaxiService(taxi_location=0.0)
    passengers = generate_random_passengers(num_passengers)

    # ground truth: who has highest welfare?
    scores = [game.score(p) for p in passengers]
    true_best_idx = max(range(len(passengers)), key=lambda i: scores[i])
    true_best = passengers[true_best_idx]

    # DP mechanism
    winner_dp, probs = exponential_dp_winner(game, passengers, epsilon)

    # deterministic VCG allocation
    winner_vcg = vcg_winner(game, passengers)

    return {
        "true_best_id": true_best.id,
        "winner_dp_id": winner_dp.id,
        "winner_vcg_id": winner_vcg.id,
        "scores": scores,
        "probs": probs,
    }

# retrurns a dictionary mapping epsilon to statistics about accuracy
def run_epsilon_sweep(num_passengers, epsilons, runs_per_eps):
    results = {}
    for eps in epsilons:
        correct_count = 0
        for _ in range(runs_per_eps):
            world = run_single_world(num_passengers, eps)
            if world["winner_dp_id"] == world["true_best_id"]:
                correct_count += 1
        accuracy = correct_count / runs_per_eps
        results[eps] = {"accuracy": accuracy}
    return results
