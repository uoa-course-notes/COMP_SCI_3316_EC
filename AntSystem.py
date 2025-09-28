from TSP import TSP, np 
from typing import Optional



class AntSystem:
    # implements the Ant System (with cycle pheromone update) algorithm for solving TSP
    def __init__(self, tsp_instance: TSP, m: int):
        self.tsp = tsp_instance  # TSP instance
        self.num_ants = m  # number of ants

        self.pheromone_taus: np.ndarray = np.ndarray([])  # pheromone matrix
        self.heuristic_etas: np.ndarray = np.ndarray([])  # heuristic information matrix (1/dist)

    def _nearest_neighbor_tour(self, start_node: int) -> tuple[int, np.ndarray]: 
        """
        Calculates a tour using the Nearest Neighbor heuristic starting from the given node.
        Returns the length of the tour and the tour itself as a numpy array.
        """
        current_node = start_node
        unvisited = set(range(self.tsp.size))
        unvisited.remove(current_node)
        tour = [current_node]
        tour_length = 0

        while unvisited: 
            min_dist = float('inf')
            next_node = -1 

            # finds the nearest unvisited neighbor
            for node in unvisited:
                dist = self.tsp.distance_matrix[current_node][node]
                if dist < min_dist:
                    min_dist = dist
                    next_node = node

            # if a next node was found, move to it
            if next_node != -1:
                tour.append(next_node)
                tour_length += min_dist
                current_node = next_node
                unvisited.remove(current_node)
            else:
                break

        # return to the starting node
        tour.append(start_node)
        tour_length += self.tsp.distance_matrix[current_node][start_node]

        return (tour_length, np.array(tour, dtype=int))


    def initialize_heuristics_info_matrix(self):
        # initialize pheromone and heuristic matrices
        self.heuristic_etas = np.zeros((self.tsp.size, self.tsp.size))

        # calculate heuristic information (1/dist) for each edge
        for i in range(self.tsp.size):
            for j in range(self.tsp.size):
                if i > j:
                    self.heuristic_etas[i][j] = 1 / self.tsp.distance_matrix[i][j]
                elif i < j:
                    self.heuristic_etas[i][j] = self.heuristic_etas[j][i]
                else:
                    self.heuristic_etas[i][j] = 0.0



    # initialize pheromone levels to a small constant value
    def compute_initial_pheromone_matrix(self, m: Optional[int] = None):
        # m: number of ants
        if m is None:
            m = self.num_ants
        min_L_nn = float('inf')
        # initial pheromone level tau_0 = m / L_nn
        for node in range(self.tsp.size):
            L_nn, _ = self._nearest_neighbor_tour(node)
            if L_nn < min_L_nn:
                min_L_nn = L_nn
        tau_0 = m / min_L_nn
        self.pheromone_taus = np.full((self.tsp.size, self.tsp.size), tau_0)



if __name__ == "__main__":
    tsp_problem = TSP()

    tsp_problem.read_tsp_file("data/eil51.tsp")
    tsp_problem.calculate_distance()
    

    num_ants = 10
    AS = AntSystem(tsp_problem, m=num_ants)
    AS.initialize_heuristics_info_matrix()
    AS.compute_initial_pheromone_matrix()
    print(f"Pheromone matrix = {AS.pheromone_taus}")
    print(f"Heuristic matrix = {AS.heuristic_etas}")

