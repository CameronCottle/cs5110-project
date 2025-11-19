All games are non-cooperative, meaning each player acts in their own self interest.
# Games being played:
- Owner vs Owner Game (OOG)
- Owner vs Collector Game (OCG)
- Owner vs Adversary (OAG)
- Collector vs Adversary (CAG)

## OOG
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

### ECG
Analyses the coordination of pseudonym changes for vehicles to protect privacy by mix zones in vehicular networks
##### Strategy
- Same as PCG
##### Payoff
- Degree of privacy
##### Equilibrium Analysis
- "It constructs a static game with complete information. By simple computation and derivation, they get the number of vehicles in Nash Equilibrium that want to change their name."

## OCG
Collectors offer location-based services or monetary profit according to location information of the former. Here, the challenge is how to motive the former to report more accurate location.

##### Strategy
- Owners: To adjust location accuracy evaluated by information entropy.
- Collectors: To design the proper incentive measures.

##### Payoff
- Owners: profit from data collectors minus privacy risk.
- Collectors: payoff is location value minus its cost.

##### Equilibrium Analysis
- The article talks about a mechinism design to find a Nash Equilibrium between the players, allowing data owners to profit and data collectors to receive accurate information. This requires more research into how we can replicate the game. Refer to page 111 of the report:
    - "They first propose a Vickrey-Clarke-Groves (VCG)-based auction protocol to select the winner of passengers. Then, an exponential differential privacy mechanism is presented to protect passengers’ privacy and allocate the winner to the taxi." 
