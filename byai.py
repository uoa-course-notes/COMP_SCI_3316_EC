from TSP import TSP, np 
from typing import Optional, List

class AntSystem:
    # implements the Ant System (with cycle pheromone update) algorithm for solving TSP
    def __init__(self, tsp_instance: TSP, m: int):
        self.tsp = tsp_instance  # TSP instance
        self.num_ants = m  # number of ants

        # Initialize as None, will be properly sized later
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
        # initialize heuristic matrices
        self.heuristic_etas = np.zeros((self.tsp.size, self.tsp.size))

        # calculate heuristic information (1/dist) for each edge
        for i in range(self.tsp.size):
            for j in range(self.tsp.size):
                if i > j:
                    dist = self.tsp.distance_matrix[i][j]
                    self.heuristic_etas[i][j] = 1.0 / dist if dist > 0 else 0.0
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

def is_Tabu_full(Tabus: List[List[int]], n: int) -> bool:
    """
    Tabus := list of visited cities for each ant
    n     := number of cities  
    """
    for tabu_k in Tabus:
        if len(tabu_k) != n:
            return False
    return True

def Transition_Probabilities(Visibility_matrix: np.ndarray, 
                             Pheromone_matrix: np.ndarray, 
                             alpha: float, 
                             beta: float, 
                             current_city: int, 
                             visited_cities: set) -> np.ndarray:
    """
    Calculate transition probabilities from current_city to unvisited cities.
    Returns a 1D array of probabilities for unvisited cities only.
    """
    n: int = len(Visibility_matrix)
    unvisited = [j for j in range(n) if j not in visited_cities]
    
    if not unvisited:
        return np.array([])
    
    # Calculate numerators for unvisited cities
    numerators = []
    for j in unvisited:
        eta_ij = Visibility_matrix[current_city, j]
        tau_ij = Pheromone_matrix[current_city, j]
        numerator = np.power(tau_ij, alpha) * np.power(eta_ij, beta)
        numerators.append(numerator)
    
    numerators = np.array(numerators)
    denominator = np.sum(numerators)
    
    # Handle zero denominator case
    if denominator == 0:
        # Uniform probability for unvisited cities
        return np.ones(len(unvisited)) / len(unvisited)
    
    probabilities = numerators / denominator
    return probabilities

def choose_next_city(probabilities: np.ndarray, unvisited_cities: List[int]) -> int:
    """
    Choose next city based on probabilities using roulette wheel selection.
    """
    if len(probabilities) == 0 or len(unvisited_cities) == 0:
        return -1
    
    # Roulette wheel selection
    rand_val = np.random.random()
    cumulative_prob = 0.0
    
    for i, prob in enumerate(probabilities):
        cumulative_prob += prob
        if rand_val <= cumulative_prob:
            return unvisited_cities[i]
    
    # Fallback: return last city
    return unvisited_cities[-1]

if __name__ == "__main__":
    # Load TSP instance
    filename = "data/eil51.tsp"
    tsp_instance = TSP()
    tsp_instance.read_tsp_file(filename)
    tsp_instance.calculate_distance()
    
    n: int = tsp_instance.size
    print(f"Problem size: {n} cities")

    # AS Algorithm parameters
    alpha: float = 1.0  # pheromone influence
    beta: float = 2.0   # heuristic influence
    rho: float = 0.5    # evaporation rate
    Q: float = 1.0      # pheromone deposit constant

    # Initialize AS
    ant_system = AntSystem(tsp_instance, m=n)  # number of ants = number of cities
    ant_system.initialize_heuristics_info_matrix()
    ant_system.compute_initial_pheromone_matrix()

    # Algorithm main loop
    t: int = 0  # time counter 
    NC: int = 0  # cycle counter 
    NCmax: int = 100  # maximum cycles

    best_tour_length = float('inf')
    best_tour = None

    print("Starting Ant System algorithm...")

    while NC < NCmax:
        # Step 1: Initialize
        # Tabu lists for each ant (list of lists)
        Tabus: List[List[int]] = [[] for _ in range(n)]
        
        # Step 2: Place m ants on n nodes
        cities = list(range(n))
        np.random.shuffle(cities)
        
        # Each ant starts at a unique city
        for k in range(n):
            start_city = cities[k]
            Tabus[k].append(start_city)
        
        # Step 3: Repeat until tabu list is full
        s: int = 1  # tabu list index
        
        while not is_Tabu_full(Tabus, n):
            for k in range(n):  # for each ant
                if len(Tabus[k]) < n:  # if ant hasn't completed tour
                    current_city = Tabus[k][-1]  # current position of ant k
                    visited_cities = set(Tabus[k])
                    
                    # Calculate transition probabilities
                    probabilities = Transition_Probabilities(
                        ant_system.heuristic_etas,
                        ant_system.pheromone_taus,
                        alpha, beta,
                        current_city,
                        visited_cities
                    )
                    
                    # Choose next city
                    unvisited = [j for j in range(n) if j not in visited_cities]
                    if unvisited:
                        next_city = choose_next_city(probabilities, unvisited)
                        if next_city != -1:
                            Tabus[k].append(next_city)
            
            s += 1
        
        # Step 4: Update pheromones
        # Calculate tour lengths for all ants
        tour_lengths = []
        for k in range(n):
            tour = np.array(Tabus[k])
            length = tsp_instance.tour_length(tour)
            tour_lengths.append(length)
            
            # Track best tour
            if length < best_tour_length:
                best_tour_length = length
                best_tour = tour.copy()
        
        # Step 5: Pheromone update
        # Evaporation
        ant_system.pheromone_taus *= (1.0 - rho)
        
        # Deposit pheromones
        for k in range(n):
            if tour_lengths[k] > 0:
                delta_tau = Q / tour_lengths[k]
                tour = Tabus[k]
                
                # Add pheromone to each edge in the tour
                for i in range(n):
                    city_from = tour[i]
                    city_to = tour[(i + 1) % n]  # wrap around to close the tour
                    ant_system.pheromone_taus[city_from][city_to] += delta_tau
                    ant_system.pheromone_taus[city_to][city_from] += delta_tau  # symmetric
        
        NC += 1
        
        # Print progress
        if NC % 10 == 0:
            avg_length = np.mean(tour_lengths)
            print(f"Cycle {NC}: Best = {best_tour_length:.1f}, Avg = {avg_length:.1f}")

    print(f"\nFinal Results:")
    print(f"Best tour length: {best_tour_length}")
    print(f"Best tour: {best_tour}")