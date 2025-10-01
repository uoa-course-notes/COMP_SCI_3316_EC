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

    def compute_initial_Taus(self, c: Optional[float] = None):
        if c is None:
            c = 0.1  # default small constant value
        self.pheromone_taus = np.full((self.tsp.size, self.tsp.size), c)

    # initialize pheromone levels to a small constant value
    def compute_initial_pheromone_matrix(self, m: int):
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




def is_Tabu_full(Tabus: np.ndarray, n: int) -> bool:
    """
    Tabus := list of visited cities 
    n     := number of cities  
    """
    is_Full: bool = True 
    for tabu_k in Tabus:
        if len(tabu_k) != n:
            is_Full = False 
            break 
    return is_Full

def Transition_Probabilities(Visibility_matrix: np.ndarray, 
                             Pheromone_matrix: np.ndarray, 
                             alpha: float, 
                             beta: float, 
                             current_city: int, 
                             unvisited_cities: set) -> np.ndarray:
    n: int = len(Visibility_matrix)

    numerators = []
    for j in unvisited_cities:
        eta_ij = Visibility_matrix[current_city, j]
        tau_ij = Pheromone_matrix[current_city, j]
        numerator = np.power(tau_ij, alpha) * np.power(eta_ij, beta)
        numerators.append(numerator)

    numerators = np.array(numerators)
    denominator = np.sum(numerators)
    probabilities = numerators/denominator
    return probabilities




# We can explore other selection methods later
def choose_next_city(probabilities: np.ndarray, unvisited_cities: set) -> tuple[int, str]:
    """
    Choose the next city to visit based on the transition probabilities.
    """
    if len(unvisited_cities) == 0 or len(probabilities) == 0:
        return -1, "No unvisited cities left or no probabilities available"
    if len(probabilities) != len(unvisited_cities):
        return -1, "Error: Mismatch between probabilities length and unvisited cities length."
    # Sample from the probability distribution
    next_city = np.random.choice(list(unvisited_cities), p=probabilities) # choose next city based on probabilities
    return next_city, ""

def is_edge_in_tabu_k(edge: tuple, tabu_k: np.ndarray) -> bool:
    """
    `edge`: is a tuple of neighboring cities (city_i, city_j)
    `tabu_k`: is an array of visited cities, which by this point is a tour.  
    """
    n = len(tabu_k)
    for city in range(n-1):
        tour_edge = (a, b) = city, city + 1
        if edge != tour_edge: return False 
    return True 


def is_stagnated(pheromone_matrix: np.ndarray, threshold: float = 1e-5) -> bool:
    """
    Check if the pheromone matrix has stagnated, i.e., all values are nearly equal.
    """
    max_tau = np.max(pheromone_matrix)
    min_tau = np.min(pheromone_matrix)
    return (max_tau - min_tau) < threshold



if __name__ == "__main__":
    tsp_instance = TSP()
    n: int = tsp_instance.size
    Distance_matrix: np.ndarray = tsp_instance.distance_matrix
    Cities = np.ndarray([i for i in range(n)])
    print(f"TSP instance with {n} cities loaded.")


    # initialize AS parameters (to be tuned)
    t: int = 0 # time counter 
    NC: int = 0 # cycle counter 
    NC_max: int = 100 # maximum number of cycles
    c = 1      # initial (t=0) trail value for each edge 

    # Initialize AS 
    ant_system = AntSystem(tsp_instance, m=n)
    ant_system.initialize_heuristics_info_matrix()
    ant_system.compute_initial_Taus(c)
    Visibility_matrix: np.ndarray = ant_system.heuristic_etas
    # deposit initial pheromone trails to each edge 
    Pheromone_matrix: np.ndarray = ant_system.pheromone_taus


    alpha: float = 1.0 # pheromone importance factor
    beta: float = 2.0  # heuristic importance factor
    rho: float = 0.5   # pheromone evaporation rate
    Q: float = 1.0     # pheromone deposit factor




    Delta_Tau = np.zeros(
                        shape=(n, n),
                        dtype=int
                    )

    # Ant initialization 
    m: int = 100 # number of ants 1 <= k <= m 




    if n == m: # same number of ants and cities 
        # assume this case for now ...
        # randomly assigns one city to each ant (without replacement)
        # one unique city per ant 
        
        while True:
            # Step 1: initialize
            # Tabu list for each ant, m of them  
            Tabus: np.ndarray = np.empty(
                shape=m,  # a 1D list of `m` lists (tabu_k) 1 <= k <= m
                dtype=np.ndarray
            )



            # Step 2: place m ants on each nodes 
            s = 0                    # tabu list index
            cities = list(range(n))
            np.random.shuffle(cities)
            # each ant_k starts at a unique city
            i = 0
            for tabu_k in Tabus:
                start_city = cities[i]
                tabu_k.append(start_city) # each tabu_k starts with one unique city
                i += 1

            
            
            # Step 3: repeat until tabu list is full
            while not is_Tabu_full(Tabus, n):
                for k in range(m): # for each ant 
                    if len(Tabus[k]) == n: # if ant_k has completed its tour
                        continue           # skip to the next ant
                    tabu_k = Tabus[k] # list of visited cities 
                    current_city = tabu_k[-1] # current city of ant k

                    unvisited_cities = np.setdiff1d(tabu_k, # list of unvisited cities
                                                    Cities, 
                                                    assume_unique=True)
                    unvisited_cities = set(unvisited_cities)

                    # calculate transition probabilities for ant_k's neighboring cities 
                    # by neighboring cities, we mean all of the adjacent cities that are not in tabu_k (that are still unvisited, or in `unvisited_cities`)
                    ant_k_transition_probabilities = Transition_Probabilities(
                                Visibility_matrix, 
                                Pheromone_matrix, 
                                alpha, beta, 
                                current_city, 
                                unvisited_cities)

                    # if there are still unvisited cities
                    if unvisited_cities:
                        # choose the city j to move to
                        next_city, error_message = choose_next_city(ant_k_transition_probabilities, unvisited_cities)
                        if error_message:
                            print(f"Error choosing next city for ant {k}: {error_message}")
                            SystemExit(1)
                        if next_city != -1:
                            # move the k-th ant to the town j
                            tabu_k.append(next_city)

                # insert city j in tabu_k(s)
                s = s + 1
                
            # By this stage, each ant's tabu list should contain 
            # a tour of length n (number of cities)



            # Step 4: update pheromones
            Ant_k_tour_length = np.zeros(shape=m, dtype=int) # tour lengths for all ants
            best_tour_length = float('inf')
            best_tour = None
            for k in range(m):
                # move ant_k from tabu_n to tabu_0
                tabu_k = Tabus[k]
                length = tsp_instance.tour_length(tabu_k)
                Ant_k_tour_length[k] = length
                if length < best_tour_length:
                    best_tour_length = length
                    best_tour = tabu_k.copy() # make a copy of the best tour found so far
            print(f"Best tour length found: {best_tour_length}")
            print(f"Best tour found: {best_tour}")

            # Determine how much pheromone each ant deposits on its tour
            for k in range(m):
                tabu_k = Tabus[k]
                length = Ant_k_tour_length[k]
                delta_tau_k = Q / length  # pheromone deposit for ant k

                # for each edge 
                for i in range(n - 1): # 0,1,2 ..., n - 2 
                    city_i = tabu_k[i]
                    city_j = tabu_k[i + 1]
                    # if the edge is in the tour described by tabu_k
                    edge: tuple = (city_i, city_j)
                    f: bool = is_edge_in_tabu_k(edge, tabu_k)
                    if f is True: Delta_Tau[city_i][city_j] += delta_tau_k
                    else:         Delta_Tau[city_i][city_j] += 0  # no pheromone is added 

            # Step 5:
            # for every edge, compute tau_ij(t + n) = (1 - rho) * tau_ij(t) + Delta_tau_ij(t)
            for i in range(n):
                for j in range(n):
                    if i > j: 
                        ant_system.pheromone_taus[i][j] = (1 - rho) * ant_system.pheromone_taus[i][j] + Delta_Tau[i][j]
                    elif i < j:
                        ant_system.pheromone_taus[i][j] = ant_system.pheromone_taus[j][i]
                    else: # i == j
                        ant_system.pheromone_taus[i][j] = 0.0


            # increment time counter
            t = t + n # after one complete cycle
            NC = NC + 1 # increment cycle counter
            print(f"Cycle {NC} completed at time {t}.")
            
            # reset Delta_Tau for the next cycle
            Delta_Tau = np.zeros(
                            shape=(n, n),
                            dtype=int
                        )
            
            NC += 1
            termination_condition = NC < NC_max and not is_stagnated(ant_system.pheromone_taus)

            if termination_condition:
                # empty all tabu lists
                for tabu_k in Tabus:
                    tabu_k.clear()
                continue # continue to the next cycle
            else:
                # print final results and exit
                print(f"Terminating at cycle {NC}. Best tour length: {best_tour_length}")
                print(f"Best tour: {best_tour}")
                exit()  # exit the while loop
    elif n > m: # less ant then cities 
        pass 
    else: # n < m: more ants than cities 
        pass 
