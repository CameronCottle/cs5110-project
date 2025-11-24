## Information about the VCG style action being played
This game is represented as an online taxi-hailing system with many passengers and at least one taxi.
- The passengers (owners):
    - want a taxi
    - are located at different locations
    - care about thier locational privacy

- The platform (collectors):
    - wants to send taxis that create the highest social value (value minus travel cost)
    - offer proper incentives to encourage accurate locational data
    - protect passenger data using differential privacy

## The auction
- Each player submits a bid and a location
- The mechnanism chooses the wunner that maximizes social welfare
- Payments follow VCG

## The trade off ε
- The trade off between privacy and accuracy is described as ε (epsilon).
- If ε is small, there is a large amount of privacy, lots of randomess, and the results are noisy
- If ε is large there is little privacy and the winner is strictly determined by their value.

## The machanism
- The mechanism is used by the platform to determine the winner of the game, aka who gets a taxi sent to them
- The mechanism uses VCG to encourage users to tell the truth about their location. Remeber that the best strategy in a VCG style auction is to bid your real price.
- The mechanism uses exponential DP to ensure privacy.
    - By using DP, the output of a randomized algorithm should not change very much when one person's data changes. This protects privacy even if an attackers knows everything else.
    - A mechanism M is ε-differentially private if for all:
        - neighboring datasets x and x prime
        - all possible outputs y
    - it holds that PR(M(x)=y)/PR(M(x)=y)<= e^ε
    - This equation means: changing one person should not make the output much more or less likely. ε small = high privacy, ε big = low privacy.
- ε controls the trade off.
    - How strongly the sore influences the winner
    - How much privacy each passenger retains
    - how much efficiency the mechanism preserves
    - How close the mechanism is to a pure VCG auction
- The winner is picked by using the equation:
    - P(i) = exp((ε)(score_i))/sum_exp((ε)score_j)
    - The highest score still is most likely to win, but not deterministically.