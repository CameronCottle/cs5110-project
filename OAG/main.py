from player import Owner, Adversary
from OAGgame import OAGGame

owner = Owner(U=3.0, P=10.0, C_p=0.4, gamma=0.1)
adv = Adversary(G=25.0, C_a=1.0)

game = OAGGame(owner, adv)

print("All profiles:")
for entry in game.all_profiles():
    print(f"{entry[0]} | {entry[1]}")
    print(f"\t    | {round(entry[2][0], 2)}  |  {round(entry[2][1], 2)} |")

pure_eqs = game.pure_equilibria()

if not pure_eqs:
    mix = game.mixed_equilibrium()
    print(mix)
    print("\nMixed Nash equilibrium (strategy probabilities):")
    for x, y in mix.items():
        print(f"{x}: {round(mix[x], 2)}")
    print()
else:
    print(f"\nPure Nash equilibria: {(pure_eqs[0][0])} | {(pure_eqs[0][1])}")
