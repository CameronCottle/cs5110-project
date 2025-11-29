from simulate import run_epsilon_sweep
from plots import (
    plot_accuracy_vs_epsilon,
    plot_welfare_vs_epsilon,
    plot_winner_histograms,
)

def main():
    num_passengers = 3
    epsilons = [0.01, 0.1, 0.5, 1.0, 2.0]
    runs_per_eps = 1000

    results = run_epsilon_sweep(num_passengers=num_passengers,
                                epsilons=epsilons,
                                runs_per_eps=runs_per_eps)

    print("Accuracy of picking the true best passenger vs epsilon:")
    for eps, stats in results.items():
        print(
            f"  epsilon={eps:.2f}: "
            f"accuracy={stats['accuracy']:.3f}, "
            f"avg_dp_welfare={stats['avg_dp_welfare']:.3f}, "
            f"avg_true_best_welfare={stats['avg_true_best_welfare']:.3f}"
        )

    # Plots for the report
    plot_accuracy_vs_epsilon(results)
    plot_welfare_vs_epsilon(results)

    # Histograms for a subset of epsilons (you can adjust this list)
    hist_epsilons = [0.01, 0.5, 2.0]
    plot_winner_histograms(num_passengers=num_passengers,
                           epsilons=hist_epsilons,
                           runs_per_eps=runs_per_eps)

if __name__ == "__main__":
    main()
