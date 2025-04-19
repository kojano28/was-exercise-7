#environment.py
import math
import tsplib95


# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
    ant_population: number of ants (m)
"""
class Environment:
    def __init__(self, rho, ant_population):

        self.rho =rho
        self.ant_population = ant_population
        
        # Initialize the environment topology (Task 1.1)
        self.problem = tsplib95.load('att48-specs/att48.tsp')
        self.locations = list(self.problem.get_nodes())
        self.n = len(self.locations)
        self.dist = {
            (i, j): self.problem.get_weight(i, j)
            for i in self.locations for j in self.locations if i != j
        }
        # Initialize the pheromone map in the environment (Task 1.1)
        self.initialize_pheromone_map()
        

    # Initialize the pheromone trails in the environment (Task 1.1)
    def initialize_pheromone_map(self):

        # build nearest neighbour tour
        unvisited = set(self.locations)
        current = unvisited.pop()
        tour = [current]
        while unvisited:
            next_node = min(unvisited, key=lambda node: self.dist[(current, node)])
            tour.append(next_node)
            unvisited.remove(next_node)
            current = next_node
        tour.append(tour[0])

        # initial pheromone level
        C_nn = sum(self.dist[(tour[i], tour[i+1])] for i in range(self.n))
        tau0 = self.ant_population / C_nn
        
        # assign  to every directed edge
        self.pheromone = {
            (i, j): tau0
            for i in self.locations
            for j in self.locations
            if i != j
        }


    # Update the pheromone trails in the environment (Task 1.2)
    def update_pheromone_map(self, ant_tours):
        # Step 1: Pheromone evaporation
        for edge in self.pheromone:
            self.pheromone[edge] *= (1 - self.rho)

        # Step 2: Pheromone update
        for tour in ant_tours:
            closed = tour + [tour[0]]
            # compute tour cost C_k
            C_k = sum(
                self.dist[(closed[i], closed[i+1])] for i in range(len(closed) - 1)
            )
            # pheromone contribution
            delta_tau = 1.0 / C_k
            # add to each edge in the tour
            for i in range(len(closed) - 1):
                edge = (closed[i], closed[i+1])
                self.pheromone[edge] += delta_tau

    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        return self.pheromone
    
    # Get the environment topology
    def get_possible_locations(self):
        return self.locations

    
