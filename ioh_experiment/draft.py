import numpy as np

# --- 1. Define a Fitness Function ---
# The goal is to maximize this function's output.
# For this example, we use OneMax: count the number of 1s.
def one_max_fitness(bitstring):
    """Calculates the fitness of a bitstring by summing its bits."""
    return np.sum(bitstring)


# --- 2. Implement the (1+1) EA Algorithm ---
def one_plus_one_ea(n, fitness_function, max_iterations=10000):
    """
    Implements the (1+1) Evolutionary Algorithm.

    Args:
        n (int): The length of the bitstring.
        fitness_function (callable): The function to evaluate solutions.
        max_iterations (int): The maximum number of generations.

    Returns:
        tuple: The best solution found, its fitness, and the number of iterations.
    """
    # Step 1: Choose s from {0, 1}^n randomly.
    current_solution = np.random.randint(0, 2, size=n)
    current_fitness = fitness_function(current_solution)

    for i in range(max_iterations):
        # The optimal fitness for OneMax is n. We can stop if we find it.
        if current_fitness == n:
            print(f"(1+1) EA found the optimum solution!")
            return current_solution, current_fitness, i

        # Step 2: Produce s' by flipping each bit of s with probability 1/n.
        # This is the core of your question.
        mutant = current_solution.copy()
        
        # We iterate through each bit.
        for j in range(n):
            # np.random.rand() gives a random float between 0.0 and 1.0.
            # This condition will be true with a probability of 1/n.
            if np.random.rand() < (1 / n):
                # Flip the bit (0 becomes 1, 1 becomes 0).
                mutant[j] = 1 - mutant[j]
        
        mutant_fitness = fitness_function(mutant)

        # Step 3: Replace s by s' if f(s') >= f(s).
        if mutant_fitness >= current_fitness:
            current_solution = mutant
            current_fitness = mutant_fitness

    # Step 4: Repeat (handled by the for loop).
    return current_solution, current_fitness, max_iterations


# --- 3. Implement the RLS Algorithm ---
def rls(n, fitness_function, max_iterations=10000):
    """
    Implements the Randomized Local Search (RLS) algorithm.

    Args:
        n (int): The length of the bitstring.
        fitness_function (callable): The function to evaluate solutions.
        max_iterations (int): The maximum number of generations.

    Returns:
        tuple: The best solution found, its fitness, and the number of iterations.
    """
    # Step 1: Choose s from {0, 1}^n randomly.
    current_solution = np.random.randint(0, 2, size=n)
    current_fitness = fitness_function(current_solution)

    for i in range(max_iterations):
        # Check for optimal solution
        if current_fitness == n:
            print(f"RLS found the optimum solution!")
            return current_solution, current_fitness, i

        # Step 2: Produce s' from s by flipping ONE randomly chosen bit.
        mutant = current_solution.copy()
        
        # Choose a single, random index to flip.
        flip_index = np.random.randint(0, n)
        mutant[flip_index] = 1 - mutant[flip_index]
        
        mutant_fitness = fitness_function(mutant)

        # Step 3: Replace s by s' if f(s') >= f(s).
        if mutant_fitness >= current_fitness:
            current_solution = mutant
            current_fitness = mutant_fitness

    # Step 4: Repeat (handled by the for loop).
    return current_solution, current_fitness, max_iterations


# --- 4. Example Usage ---
# if __name__ == "__main__":
    # # Problem parameters
    # N_BITS = 100         # Length of the bitstring
    # MAX_ITERATIONS = 20000 # Safety stop for the "forever" loop

    # print(f"--- Running Optimization for a Bitstring of Length {N_BITS} ---")
    # print(f"Goal: Find a string of all 1s (Fitness = {N_BITS})\n")

    # # Run (1+1) EA
    # print("Running (1+1) EA...")
    # best_sol_ea, best_fit_ea, iters_ea = one_plus_one_ea(N_BITS, one_max_fitness, MAX_ITERATIONS)
    # print(f"Result: Fitness of {best_fit_ea}/{N_BITS} reached in {iters_ea} iterations.")
    # # print(f"Final Solution: {best_sol_ea}\n") # Uncomment to see the bitstring

    # print("-" * 20)

    # # Run RLS
    # print("Running RLS...")
    # best_sol_rls, best_fit_rls, iters_rls = rls(N_BITS, one_max_fitness, MAX_ITERATIONS)
    # print(f"Result: Fitness of {best_fit_rls}/{N_BITS} reached in {iters_rls} iterations.")
    # # print(f"Final Solution: {best_sol_rls}") # Uncomment to see the bitstring
X = np.random.randint(0, 2, 10)
print(X)