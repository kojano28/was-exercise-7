#ant_colony.py
import numpy as np

from environment import Environment
from ant import Ant 

# Class representing the ant colony
"""
    ant_population: the number of ants in the ant colony
    iterations: the number of iterations 
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
    rho: pheromone evaporation rate
"""
class AntColony:
    def __init__(self, ant_population: int, iterations: int, alpha: float, beta: float, rho: float):
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho 

        # Initialize the environment of the ant colony
        self.environment = Environment(self.rho, self.ant_population)

        # Initialize the list of ants of the ant colony
        self.ants = []

        # Initialize the ants of the ant colony
        for i in range(ant_population):
            
            # Initialize an ant on a random initial location 
            ant = Ant(self.alpha, self.beta, None)

            # Position the ant in the environment of the ant colony so that it can move around
            ant.join(self.environment)
        
            # Add the ant to the ant colony
            self.ants.append(ant)

    # Solve the ant colony optimization problem  (Task 2.3)
    def solve(self):

        solution, shortest_distance = None, np.inf         
        for _ in range(self.iterations):
            ant_tours = []                        

            for ant in self.ants:
                ant.join(self.environment)         
                tour = ant.run()                   
                ant_tours.append(tour)

                if ant.traveled_distance < shortest_distance:
                    shortest_distance = ant.traveled_distance
                    solution = tour

        # update the environment
            self.environment.update_pheromone_map(ant_tours)

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    ant_colony= AntColony(
        ant_population=48,
        iterations=200,
        alpha=1.0,
        beta=3.0,
        rho=0.5
    )

    # Solve the ant colony optimization problem
    solution, shortest_distance = ant_colony.solve()
    print("Solution: ", solution)
    print("Distance: ", shortest_distance)


if __name__ == '__main__':
    main()    