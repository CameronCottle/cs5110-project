from params import default_params
from simulate import run_p_sweep


def main():
    params = default_params()
    PValues = [1, 2, 3, 4, 5, 6, 7, 8]

    # run the p sweep to run the game for different p values
    results = run_p_sweep(PValues, params)

    print("CAG mixed equilibrium & leakage vs p:")
    for p in PValues:
        stats = results[p]
        print(
            f"  p={p:2d} | x*={stats['x_star']:.3f} (DC plays P) "
            f"| y*={stats['y_star']:.3f} (ADV plays E) "
            f"| leak={stats['leakage_prob']:.3f} "
            f"| DC={stats['dc_payoff']:.3f} | ADV={stats['adv_payoff']:.3f}"
        )

if __name__ == "__main__":
    main()
