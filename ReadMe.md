All games are non-cooperative, meaning each player acts in their own self interest.
# Games being played:
- Owner vs Owner Game (OOG) - TBD
- Owner vs Collector Game (OCG) - Cameron
- Owner vs Adversary (OAG) - Ethan
- Collector vs Adversary (CAG) - TBD

## OOG (Gavin)
The OOG game is played as a Pseudonym Change Game (PCG), External C-Game for Privacy (ECG), Dummy User generation game, Tragectory Privacy Preservation Game, and Collaberative Location Privacy Game. 

### PCG
Read more about PSG here https://pmc.ncbi.nlm.nih.gov/articlesPMC9141923/.

##### Strategy
- Cooperation
    - "Once some data owner adopts this strategy, he/she needs to change some pseudonym in multipletimes. Meanwhile, it causes a certain amount of cost, i.e., utility loss." 
- Defection
    - Does nothing, but the risk of location identification increases.
##### Payoff
- Refer to the table on page 110 of the report
##### Equilibrium Analysis
- the cost of changing pseudonym and the number of players influence the achievement of high location privacy.
- It really depends if the other players move is known.


## OCG (Cameron)
Collectors offer location-based services or monetary profit according to location information of the former. Here, the challenge is how to motive the former to report more accurate location. The game here is played as a Privacy Game Between Owners and Collectors (PGOC).

### PGOC
Information about the game here https://link.springer.com/chapter/10.1007/11681878_14. 

##### Strategy
- Owners: To adjust location accuracy evaluated by information entropy.
- Collectors: To design the proper incentive measures.

##### Payoff
- Owners: profit from data collectors minus privacy risk.
- Collectors: payoff is location value minus its cost.

##### Equilibrium Analysis
- The article talks about a mechinism design to find a Nash Equilibrium between the players, allowing data owners to profit and data collectors to receive accurate information. This requires more research into how we can replicate the game. Refer to page 111 of the report:
    - "They first propose a Vickrey-Clarke-Groves (VCG)-based auction protocol to select the winner of passengers. Then, an exponential differential privacy mechanism is presented to protect passengers’ privacy and allocate the winner to the taxi." 

## OAG (Ethan)
The OAG game is played as a **Game Between Users and Adversaries (GUA)**.

### GUA
The Game Between Users and Adversaries (GUA) is a game with the Owners deciding to Cooperate or Defect, while the Adversary attacks or abstains.

##### Strategy
- **Owners:**
  - **Cooperate = Protect:** apply a privacy mechanism, this is privacy but has a cost.
  - **Defect = Do nothing:** save the cost but increase the risk of losing data.
- **Adversaries:**
  - **Attack:** eavesdrop/track to infer locations; this has an attack.
  - **Abstain:** don’t attack; no cost, no gain.

##### Payoff (in words)
- **Owner protects, adversary attacks:** the owner keeps service utility but pays the protection cost, the adversary gains from the attempt but pays the attack.
- **Owner protects, adversary abstains:** the owner enjoys utility but still pays the protection cost, the adversary gets nothing.
- **Owner defects, adversary attacks:** the owner doesn’t pay for protection but loses privacy/utility to the attack the adversary gains minus their attack.
- **Both do nothing:** neither side gains nor pays any.

##### Equilibrium Analysis
- I believe there is a Nash equilibrium **(Owner protects, Adversary abstains)** or **(Owner defects, Adversary abstains)** which is caused by the relative sizes of protection and attack costs.

### CAG
info here about the game
