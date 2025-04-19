# ant.py
import random
from environment import Environment

# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location
        self.traveled_distance = 0
        self.environment: Environment
        self.unvisited = set()

    # The ant runs to visit all the possible locations of the environment (Task 2.2)
    def run(self):
        tour = [self.current_location]
        while self.unvisited:
            tour.append(self.select_path())
        self.traveled_distance += self.get_distance(self.current_location, tour[0])
        return tour

    # Select the next path based on the random proportional rule of the ACO algorithm (Task 2.1)
    def select_path(self):
        i = self.current_location
        pheromone = self.environment.get_pheromone_map()
        weights = []

        # compute weight for each candidate
        for j in self.unvisited:
            tau = pheromone[(i, j)]
            distance = self.get_distance(i, j)
            eta = 1.0 / distance
            weight = (tau ** self.alpha) * (eta ** self.beta)
            weights.append((j, weight))

        # sum of weights
        total = sum(w for _, w in weights)

        # roulette-wheel selection
        r = random.random() * total
        cumulative = 0.0
        for loc, w in weights:
            cumulative += w
            if r <= cumulative:
                next_loc = loc
                break

        # update state
        self.traveled_distance += self.get_distance(i, next_loc)
        self.current_location = next_loc
        self.unvisited.remove(next_loc)
        return next_loc

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment
        self.unvisited = set(environment.get_possible_locations())
        self.current_location = random.choice(list(self.unvisited)) if self.current_location is None or self.current_location not in self.unvisited else self.current_location
        self.unvisited.remove(self.current_location)
        self.traveled_distance = 0.0

    # enabling an ant to compute the pseudo-euclidean distance between two cities. (Task 2.1)
    def get_distance(self, i, j):
        return self.environment.dist[(i, j)]
