import matplotlib.pyplot as plt
from simulate import sample_dp_winners

def plot_accuracy_vs_epsilon(results):
    epsilons = sorted(results.keys())
    accuracies = [results[eps]["accuracy"] for eps in epsilons]

    plt.figure(figsize=(7, 5))
    plt.plot(epsilons, accuracies, marker="o")
    plt.xlabel("Privacy Parameter ε")
    plt.ylabel("Accuracy (P(DP winner = true best))")
    plt.title("Effect of ε on Allocation Accuracy")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_welfare_vs_epsilon(results):
    epsilons = sorted(results.keys())
    dp_welfare = [results[eps]["avg_dp_welfare"] for eps in epsilons]
    optimal_welfare = [results[eps]["avg_true_best_welfare"] for eps in epsilons]

    plt.figure(figsize=(7, 5))
    plt.plot(epsilons, optimal_welfare, marker="o", label="Optimal welfare (true best)")
    plt.plot(epsilons, dp_welfare, marker="o", label="DP mechanism welfare")
    plt.xlabel("Privacy Parameter ε")
    plt.ylabel("Expected Welfare (score)")
    plt.title("Welfare vs. Privacy Level ε")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_winner_histograms(num_passengers, epsilons, runs_per_eps):
    num_eps = len(epsilons)
    fig, axes = plt.subplots(1, num_eps, figsize=(4 * num_eps, 4), sharey=True)

    # handle case where there's only 1 epsilon
    if num_eps == 1:
        axes = [axes]

    for ax, eps in zip(axes, epsilons):
        winners = sample_dp_winners(num_passengers, eps, runs_per_eps)
        ax.hist(winners, bins='auto', rwidth=0.8)
        ax.set_title(f"ε = {eps}")
        ax.set_xlabel("Winner passenger ID")
        ax.set_ylabel("Count")

    plt.suptitle("Distribution of DP Winners for Different ε")
    plt.tight_layout()
    plt.show()
