# main.py (full example)
from Owner import DataOwner

A_SUCCESS = 1.0  # log2(2) for 2 players


def build_freudiger_payoffs_2player(p1: DataOwner, p2: DataOwner):
    u1_minus = p1.u
    u2_minus = p2.u
    gamma = p1.gamma  # assume same γ

    u1_CC = A_SUCCESS - gamma
    u2_CC = A_SUCCESS - gamma

    u1_CD = max(0.0, u1_minus - gamma)
    u2_CD = u2_minus

    u1_DC = u1_minus
    u2_DC = max(0.0, u2_minus - gamma)

    u1_DD = u1_minus
    u2_DD = u2_minus

    p1_payoffs = [[u1_CC, u1_CD],
                  [u1_DC, u1_DD]]
    p2_payoffs = [[u2_CC, u2_DC],
                  [u2_CD, u2_DD]]

    return p1_payoffs, p2_payoffs


def run_sim(num_rounds: int = 20):
    actions = ["C", "D"]
    opp_actions = ["C", "D"]

    # You can swap 'best_response' with 'threshold' here.
    p1 = DataOwner("P1", actions=actions, policy="best_response",
                   gamma=0.3, lambda_loss=0.05, initial_privacy=A_SUCCESS)
    p2 = DataOwner("P2", actions=actions, policy="best_response",
                   gamma=0.3, lambda_loss=0.05, initial_privacy=A_SUCCESS)

    for t in range(1, num_rounds + 1):
        # Location privacy decays between games (β_i grows)
        p1.apply_privacy_loss()
        p2.apply_privacy_loss()

        # Build payoff matrices using current u1⁻, u2⁻
        p1_payoffs, p2_payoffs = build_freudiger_payoffs_2player(p1, p2)

        # Each player chooses C or D
        a1 = p1.choose_action(p1_payoffs, opp_actions)
        a2 = p2.choose_action(p2_payoffs, opp_actions)

        i1 = 0 if a1 == "C" else 1
        j1 = 0 if a2 == "C" else 1
        i2 = 0 if a2 == "C" else 1
        j2 = 0 if a1 == "C" else 1

        u1_new = p1_payoffs[i1][j1]
        u2_new = p2_payoffs[i2][j2]

        # Update each owner's internal state & cumulative score
        p1.observe_outcome(a1, a2, u1_new)
        p2.observe_outcome(a2, a1, u2_new)

        print(f"Round {t:02d}: P1={a1} (u={u1_new:.3f}) | P2={a2} (u={u2_new:.3f})")

    print("\nFinal internal payoffs (u):", p1.u, p2.u)
    print("Cumulative scores:", p1.total_score, p2.total_score)


if __name__ == "__main__":
    run_sim()
