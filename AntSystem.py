from TSP import TSP, np 
# from typing import Optional



# class AntSystem:
#     # implements the Ant System (with cycle pheromone update) algorithm for solving TSP
#     def __init__(self, tsp_instance: TSP, m: int):
#         self.tsp = tsp_instance  # TSP instance
#         self.num_ants = m  # number of ants

#         self.pheromone_taus: np.ndarray = np.ndarray([])  # pheromone matrix
#         self.heuristic_etas: np.ndarray = np.ndarray([])  # heuristic information matrix (1/dist)

#     def _nearest_neighbor_tour(self, start_node: int) -> tuple[int, np.ndarray]: 
#         """
#         Calculates a tour using the Nearest Neighbor heuristic starting from the given node.
#         Returns the length of the tour and the tour itself as a numpy array.
#         """
#         current_node = start_node
#         unvisited = set(range(self.tsp.size))
#         unvisited.remove(current_node)
#         tour = [current_node]
#         tour_length = 0

#         while unvisited: 
#             min_dist = float('inf')
#             next_node = -1 

#             # finds the nearest unvisited neighbor
#             for node in unvisited:
#                 dist = self.tsp.distance_matrix[current_node][node]
#                 if dist < min_dist:
#                     min_dist = dist
#                     next_node = node

#             # if a next node was found, move to it
#             if next_node != -1:
#                 tour.append(next_node)
#                 tour_length += min_dist
#                 current_node = next_node
#                 unvisited.remove(current_node)
#             else:
#                 break

#         # return to the starting node
#         tour.append(start_node)
#         tour_length += self.tsp.distance_matrix[current_node][start_node]

#         return (tour_length, np.array(tour, dtype=int))


#     def initialize_heuristics_info_matrix(self):
#         # initialize pheromone and heuristic matrices
#         self.heuristic_etas = np.zeros((self.tsp.size, self.tsp.size))

#         # calculate heuristic information (1/dist) for each edge
#         for i in range(self.tsp.size):
#             for j in range(self.tsp.size):
#                 if i > j:
#                     self.heuristic_etas[i][j] = 1 / self.tsp.distance_matrix[i][j]
#                 elif i < j:
#                     self.heuristic_etas[i][j] = self.heuristic_etas[j][i]
#                 else:
#                     self.heuristic_etas[i][j] = 0.0



#     # initialize pheromone levels to a small constant value
#     def compute_initial_pheromone_matrix(self, m: Optional[int] = None):
#         # m: number of ants
#         if m is None:
#             m = self.num_ants
#         min_L_nn = float('inf')
#         # initial pheromone level tau_0 = m / L_nn
#         for node in range(self.tsp.size):
#             L_nn, _ = self._nearest_neighbor_tour(node)
#             if L_nn < min_L_nn:
#                 min_L_nn = L_nn
#         tau_0 = m / min_L_nn
#         self.pheromone_taus = np.full((self.tsp.size, self.tsp.size), tau_0)




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


def choose_next_city():
    pass 




if __name__ == "__main__":
    tsp_instance = TSP()
    n: int = tsp_instance.size
    Distance_matrix: np.ndarray = tsp_instance.distance_matrix
    Cities = np.ndarray([i for i in range(n)])


    # initialize 
    t: int = 0 # time counter 
    NC: int = 0 # cycle counter 
    c = 1      # initial (t=0) trail value for each edge 

    # deposit initial pheromone trails to each edge 
    Tau: np.ndarray = np.ndarray([]) # pheromone matrix 

    for i in range(n):
        for j in range(n):
            if i < j: 
                Tau[i, j] = c
            elif i == j: Tau[i,j] = c
            else: # i > j
                Tau[i, j] = Tau[j, i]


    #
    # 
    Delta_Tau = np.zeros(
                        shape=(n, n),
                        dtype=int
                    )

    # Ant initialization 
    m: int = 100 # number of ants 1 <= k <= m 


    # Tabu list for each ant, m of them  
    Tabus: np.ndarray = np.empty(
        shape=m, # a 1D list of `m` lists (tabu_k) 1 <= k <= m
        dtype=np.ndarray
    )


    if n == m: # same number of ants and cities 
        # assume this case for now ...
        # randomly assigns one city to each ant (without replacement)
        # one unique city per ant 
        
        
        
        # Step 2: place m ants on each nodes 
        s = 0                    # tabu list index
        cities = list(range(n))
        np.random.shuffle(cities)

         # each ant k starts at a unique city
        i = 0
        for tabu_k in Tabus:
            tabu_k = cities[i] # each tabu_k starts with one unique city
            i += 1
        
        # Step 3
        while not is_Tabu_full(Tabus, n):
            s = s + 1
            for k in range(m): # for each ant 
                tabu_k = Tabus[k] # list of visited cities 
                unvisited_cities = np.setdiff1d(tabu_k, 
                                                Cities, 
                                                assume_unique=True)
                # choose the city j to move to   
                next_city = choose_next_city()
                # next_city_j = 
                # move the k-th ant to the town j 

                # insert city j in tabu_k(s)
                pass 



    elif n > m: # less ant then cities 
        pass 
    else: # n < m: more ants than cities 
        pass 
