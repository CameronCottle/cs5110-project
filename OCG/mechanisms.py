import math
import random

# classic VCG winner selection
def vcg_winner(game, passengers):
    scores = [(p, game.score(p)) for p in passengers]
    winner, _ = max(scores, key=lambda x: x[1])
    return winner

# winner using exponential DP mechanism. returns winner and the probabilites used
def exponential_dp_winner(game, passengers, epsilon):
    scores = [game.score(p) for p in passengers]

    # compute weights
    weights = [math.exp(epsilon * s) for s in scores]
    total = sum(weights)
    probs = [w / total for w in weights]

    # sample from categorical distribution
    r = random.random()
    collective = 0.0
    for p, prob in zip(passengers, probs):
        collective += prob
        if r <= collective:
            # print(f"Selected passenger {p.id} with probability {prob:.4f} out of {probs}")
            return p, probs

    # fallback (due to tiny rounding errors)
    return passengers[-1], probs
