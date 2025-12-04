## Information about the game/file structure

### The Hide and Seek game (HSG)

This game models the interaction between two players:

- A trusted data collector (DC)
    - The DC aggregates user location requests to protect privacy
- An adversary
    - The adversary tries to track a specific users true location

### main.py

This is the main file (as seen in the name). This is the file, when ran, will output the results of the CAG style game.

### simulate.py

This file contains one function run_p_sweep. run_p_sweep plays the normal form game for different p values, as passed through. It does this by:
- building the payoff matrix
- computing the mixed equlibrium
- computing the equlibrum metrics
Refer to mechinism.py for an explanation on how the calculations are preformed.

### mechanism.py

This file contains the mechisism classes and functions to run the game, and make calculations.

#### PayOffMatrix2x2
This class is the container for the normal form game as it stores the both players payoffs.

- dc[row][col] is the data collectors payoff for that action profile in question
- adv[row][col] is the adversaries payoff for the profile in question

Consider the players moves as defined in the report:
- (P, E) = (row=0, col=0)
- (P, T) = (row=0, col=1)
- (T, E) = (row=1, col=0)
- (T, T) = (row=1, col=1)

The function payoff within this class has:
Input:

- dcAction: "P" or "T"
- advAction: "E" or "T"

Output:

(dcPayoff, advPayoff) for that action pair.

Internally:

- Converts actions into row/col indices using the convention above.
- Looks up the payoffs from the matrices.

Conceptually this class is the encapsulated game, separate from any equilibrium logic.

#### MixedEquilibrium2x2

This class is a simple data holder for the mixed Nash equilibrium of the 2×2 game. This doesn't compute anything, it just holds xStar and yStar.
- x_star: probability DC plays row 0 (P)
- y_star: probability ADV plays column 0 (E)

#### build_payoff_matrix
When given p (privacy parameter, which the is the aggregation threshold) and params (all the economic/technical parameters), this function builds the full 2x2 game that for p. It returns the payoff matrix.

Note the following is the payoff definitions:
Note the following are the payoff definitions used to construct the payoff matrix:

(P, E)
- **ADV payoff:**  
  `V * probProtectSuccess - C_E`  
- **DC payoff:**  
  `dcBenefitP - dcCostP - L * probProtectSuccess`

(P, T)
- **ADV payoff:**  
  `0`  
- **DC payoff:**  
  `dcBenefitP - dcCostP`

(T, E)
- **ADV payoff:**  
  `V * q_T - C_E`  
- **DC payoff:**  
  `B_priv_T - C_T - L * q_T`

(T, T)
- **ADV payoff:**  
  `0`  
- **DC payoff:**  
  `B_priv_T - C_T`


#### compute_mixed_equilibrium
This function compute the interior mixed-strategy Nash equilibrium of a 2x2 game. This function uses the standard indifference conditions, which are:
- ADV indifferent between E and T ⇒ solve for x*
- DC indifferent between P and T ⇒ solve for y*

- Strategies:
    - DC:  row 0 = P, row 1 = T
    - ADV: col 0 = E, col 1 = T
- Let DC payoff matrix be:
    - [ a  b ]
    - [ c  d ]

- Let ADV payoff matrix be:
    - [ e  f ]
    - [ g  h ]

This function is pretty long, so here is a step by step:
1. Extract payoffs into scalars
    - DC: a, b, c, d
    - ADV: e, f, g, h
2. Solve ADV’s indifference condition (to get x*):
    - Expected payoff of E = expected payoff of T.
    - Rearrange to solve for xStar.
3. Solve DC’s indifference condition (to get y*):
    - Expected payoff of P = expected payoff of T.
    - Rearrange to solve for y_star.
4. if the denominators are ~0, or if x* or y* fall outside [0,1], it raises an error, meaning there is no interior mixed equilibrium for this game

#### equilibrium_metrics_from_mixed
This function takes the equilibrium strategies and the game and turns them into interpretable metrics such as:
- How often DC protects (x*)
- How often ADV attacks (y*)
- The probability of a successful deanonymization (“leakage”)
- Expected DC and ADV payoffs

The inputs are 
- aggregation threshold p
- model parameters
- a 2x2 payoff matrix for (DC, ADV)
- an interior mixed equilibrium (x*, y*)

Finally, this function returns (plus p, x*, y*) as a dict.

### params.py
This file defines all parameters that describe the economics and privacy behavior of the CAG.

#### GameParams class
This class stores every numeric component needed by the payoff formulas in mechanisms.py.
- advValueSuccess: Value obtained by the adversary from a successful deanonymization attack. Higher this value is, the more incentive the adv has to attack.
- advAttackCost: Cost incurred by the adversary to launch an attack (“Exploit”). If cost is greater than or equal to reward, the adv won't attack.
- successProbTransparent: Probability an attack succeeds if the data collector does not protect (DC plays T). Think of this as the baseline vulnerability level of the system.
- dcLossOnBreach: Loss suffered by the Data Collector when an attack succeeds.
- dcPrivacyBenefitTransparent: Baseline privacy benefit when the Data Collector does not protect (T).
- dcCostTransparent: Processing cost when DC plays T. This is typically low because transparency is cheap.

The following parameters define how the system changes when p increases.
- alpha: Controls how fast attack success under protection decreases with p.
- beta: Controls how fast attack success under protection decreases with p.
- gamma: Controls how fast the cost of protection grows with p.

The following are the methods contains in params.py:
- successProbProtected(self, p): Probability an adversary succeeds when the DC protects using threshold p.
- dcPrivacyBenefitProtected(self, p): Privacy benefit increases linearly with aggregation threshold p.
- dcCostProtected(self, p): Protecting user privacy gets more expensive as p increases.

### players.py
This is the file where the players are defined (shocker I know). The players for this game are data collectors and adversaries.

Note that players.py does not compute payoffs or equilibrium.
It simply defines who the players are and what strategy choices they can make.

At the top of the file I defined strong type hints. This just makes the code safer and easier to read.

#### DataCollector class
This class represents the trusted data collector, whose job is to:
- Aggregate user requests
- Provide privacy via a fixed threshold p
- Choose between P (Protect) and T (Transparent)

#### Adversary class
This class represents the attacker who:
- Attempts deanonymization (E)
- Or chooses not to attack (T)

#### choose_action(self, x)
This function lets you simulate the game dynamics rather than just compute equilibria.