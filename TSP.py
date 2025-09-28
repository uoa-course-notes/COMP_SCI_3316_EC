import numpy as np

class TSP:
    def __init__(self):
        self.coords = {}
        self.size = 0
        self.distance_matrix: np.ndarray = np.array([])

    # getter method 
    def get_coords(self):
        return self.coords

        

    def read_tsp_file (self, filename) -> None:
        """
        Reads a TSP file and populates the TSP object with coordinates.
        This version is refactored to be more robust.
        """
        with open(filename, 'r') as file:
            lines = file.readlines()

        node_section_start = False
        temp_coords = {}
        for line in lines:
            line = line.strip() # remove white space trailing
            
            if line == "NODE_COORD_SECTION":
                node_section_start = True
                continue
            
            if line == "EOF":
                break
            
            if node_section_start:
                seq_num = line.split()
                if len(seq_num) == 3:
                    # Convert node_id to int, x and y to float
                    node_id, x, y = int(seq_num[0]), float(seq_num[1]), float(seq_num[2])
                    # Store coordinates using 0-based indexing
                    temp_coords[node_id - 1] = (x, y)

        self.coords = temp_coords
        self.size = len(self.coords)
        # Initialize distances matrix once after all nodes are read
        self.distance_matrix = np.zeros((self.size, self.size), dtype=float)

    def _euclidean_distance(self, vertex1_indx, vertex2_indx) -> int:
        return int(np.linalg.norm(np.array(self.coords[vertex1_indx]) - np.array(self.coords[vertex2_indx])))

    def calculate_distance(self):
        for row in range(self.size):
            for col in range(self.size):
                if row > col:
                    self.distance_matrix[row][col] = self._euclidean_distance(row, col)
                elif row == col:
                    self.distance_matrix[row][col] = 0.0
                else: # row < col
                    self.distance_matrix[row][col] = self.distance_matrix[col][row]


    def print_distances(self):
        for row in self.distance_matrix:
            print(row)
    

    def tour_length(self, route: np.ndarray) -> int:
        distMatrix = self.distance_matrix
        if route is None or len(route) == 0:
            print(f"Error: The route is empty or None.")
            return 0

        length = distMatrix[route[0]][route[len(route) - 1]]
        for i in range(len(route) - 1) :
            length += distMatrix[route[i]][route[i+1]]

        return int(length)
    


if __name__ == "__main__":
    filename = "data/eil51.tsp"

    tsp = TSP()
    tsp.read_tsp_file(filename)
    tsp.calculate_distance()
    
    print(f"Coordinates = {tsp.coords} of size = {tsp.size}")
    print("\nDistance matrix:")
    print(f"Distance matrix = {tsp.distance_matrix}")


    random_tour = np.random.permutation(tsp.size)
    print("\nInitial/Random Tour:", random_tour)
    print("Default tour length =", tsp.tour_length(random_tour)) 


