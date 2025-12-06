from OAGgame import OAGGame
from player import Owner, Adversary

def sweep_Cp_Ca(U, P, G, gamma, Cp_vals, Ca_vals):
    results = []

    for C_p in Cp_vals:
        for C_a in Ca_vals:
            owner = Owner(U=U, P=P, C_p=C_p, gamma=gamma)
            adversary = Adversary(G=G, C_a=C_a)
            game = OAGGame(owner, adversary)

            eq = game.pure_equilibria()

            if len(eq) == 0:
                label = "no_pure_eq"
            elif len(eq) > 1:
                label = "multiple"
            else:
                label = f"{eq[0][0].name}_{eq[0][1].name}"

            results.append((C_p, C_a, label))

    return results
