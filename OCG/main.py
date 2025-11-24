from simulate import run_epsilon_sweep

def main():
    epsilons = [0.01, 0.1, 0.5, 1.0, 2.0]
    results = run_epsilon_sweep(num_passengers=3, epsilons=epsilons, runs_per_eps=1000)

    print("Accuracy of picking the true best passenger vs epsilon:")
    for eps, stats in results.items():
        print(f"  epsilon={eps:.2f}: accuracy={stats['accuracy']:.3f}")

if __name__ == "__main__":
    main()
