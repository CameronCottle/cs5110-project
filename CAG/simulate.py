from mechanisms import compute_mixed_equilibrium, build_payoff_matrix, equilibrium_metrics_from_mixed

# runs the game for different values for p to find the equlibrium between the data collector and adversary
def run_p_sweep(pValues, params):
    results = {}
    for p in pValues:
        # build separate DC and ADV payoff matrices
        dcMatrix, advMatrix = build_payoff_matrix(p, params)

        # compute mixed-strategy equilibrium (x*, y*)
        xStar, yStar = compute_mixed_equilibrium(dcMatrix, advMatrix)

        # compute leakage and expected payoffs at equilibrium
        metrics = equilibrium_metrics_from_mixed(p, params, dcMatrix, advMatrix, xStar, yStar)
        results[p] = metrics
    return results
