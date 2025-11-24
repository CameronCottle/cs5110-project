from dataclasses import dataclass
import random

@dataclass
class Passenger:
    id: int
    value: float
    location: float

class TaxiGame:
    def __init__(self):
        self.taxi_location = 0.0

    # calculate the distance cost for a passenger
    def distance_cost(self, p: Passenger) -> float:
        return abs(p.location - self.taxi_location)

    # calculate the score for a passenger
    def score(self, p: Passenger) -> float:
        """Welfare / quality function: value - distance cost."""
        return p.value - self.distance_cost(p)

# generates random passengers in an array
def generate_random_passengers(n):
    passengers = []
    for i in range(n):
        value = random.uniform(5, 15)
        location = random.uniform(0, 10)
        passengers.append(Passenger(i, value, location))
    return passengers
