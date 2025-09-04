from TSPLib import np
import statistics as stats
import os

class Output:
    """
    Utility class to handle experiment output for TSP evolutionary runs.

    - Ensures results directory exists.
    - Appends run results (tour length, operator, filename).
    - Computes and logs summary statistics (min, mean, std).
    """

    def __init__(self):
        # Path of output file
        self.__path = "./results/algorithm.txt"

        # Ensure directory exists before writing
        self.__dir = os.path.dirname(self.__path)
        if self.__dir and not os.path.exists(self.__dir):
            os.makedirs(self.__dir)

        # Buffer for storing the last output info
        self.__info = None
    
    def __output(self, length: int, index: int, op: str, filename: str):
        """
        Internal method: format and write a single run result to file.
        
        Args:
            length   : tour length achieved
            index    : run index (0-based, but stored as 1-based in file)
            op       : operator used (e.g., '2-opt', 'pmx')
            filename : problem instance filename
        """
        # Format: "Run <index> with <op> from <filename> tour length: <length>"
        self.__info = f"Run {index + 1} with {op} from {filename} tour length: {length}\n"

        # Append to the results file
        with open(self.__path, "a") as f:
            f.write(self.__info)

    def output(self, length: int, index: int, op: str, filename: str):
        """
        Public wrapper for writing run result.
        Handles exceptions gracefully.
        """
        try:
            self.__output(length, index, op, filename)
        except Exception as e:
            print(f"Error writing to file: {e}")

    def stats(self, array: np.ndarray):
        """
        Compute and write statistics for a series of run results.

        Args:
            array: numpy array of tour lengths (one per run)

        Statistics written:
            - Minimum value
            - Mean value
            - Standard Deviation
        """
        self.__info = f"Minimum: {np.min(array)}\n"
        self.__info += f"Mean: {np.mean(array)}\n"
        self.__info += f"SD: {np.std(array)}\n\n"

        # Append stats block to results file
        with open(self.__path, "a") as f:
            f.write(self.__info)