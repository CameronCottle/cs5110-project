from mechanisms import compute_mixed_equilibrium, build_payoff_matrix, equilibrium_metrics_from_mixed

# runs the game for different values for p to find the equlibrium between the data collector and adversary
def run_p_sweep(PValues, params):
    results = {}
    for p in PValues:
        matrix = build_payoff_matrix(p, params)
        eq = compute_mixed_equilibrium(matrix)
        metrics = equilibrium_metrics_from_mixed(p, params, matrix, eq)
        results[p] = metrics
    return results
