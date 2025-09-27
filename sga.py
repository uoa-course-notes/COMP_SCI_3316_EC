# Simple Genetic Algorithm (SGA) implementation in Python
# The algorithm goes as follows: 
# Select parents for the mating pool (size of the mating pool = population size)
# Shuffle the mating pool
# For each consecutive pair, apply crossover with a certain probability p_c, otherwise copy the parents
# For each offspring, apply mutation (bit-flip with probability p_m for each bit) 
# Replace the whole population with the new offspring


import numpy as np
import random

def select_parents(population):
    # Select parents for the mating pool
    # return random.choices(population, k=len(population)) # Select with replacement
    return np.random.choice(
        a = population, 
        size=len(population), 
        replace=True,
    )

def shuffle_mating_pool(mating_pool):
    # Shuffle the mating pool
    np.random.shuffle(mating_pool) # In-place shuffling
    return mating_pool



def crossover(parents, p_c):
    # Apply crossover with probability p_c
    offspring = []
    for i in range(0, len(parents), 2):
        if i + 1 < len(parents) and random.random() < p_c:
            # Apply crossover
            point = random.randint(1, len(parents[i]) - 1)
            child1 = np.concatenate((parents[i][:point], parents[i + 1][point:]))
            child2 = np.concatenate((parents[i + 1][:point], parents[i][point:]))
            offspring.extend([child1, child2])
        else:
            # Copy parents
            offspring.extend([parents[i], parents[i + 1]])
    return offspring

def mutate(offspring, p_m):
    # Apply mutation (bit-flip) with probability p_m
    for i in range(len(offspring)):
        if random.random() < p_m:
            bit = random.randint(0, len(offspring[i]) - 1)
            offspring[i][bit] = 1 - offspring[i][bit]
    return offspring




# Evaluations 
def evaluate_individual_objective(individual: np.ndarray) -> int:

    return 0 

def evaluate_population_fitness(population) -> np.ndarray:
    scores: list = []
    for ind in population:
        scores.append(evaluate_individual_objective(ind))
    return np.ndarray(scores)




# tournament selection (can be changed later on)
def selection(pop, scores, k = 3):
    pop_size: int = len(pop)
    selection_indices: np.ndarray = np.random.choice(
        a=pop_size, 
        size=k,
        replace=False
    )

    for idx in np.random.randint(0, pop_size, k-1):
        # check if the score is better 
        if scores[idx] < scores[selection_indices]:
            selection_indices = idx 
    return population[selection_indices]


# perform crossover between two parents to create two children  
def crossover(parent_1: np.ndarray, parent_2: np.ndarray, p_c: int | float) -> tuple[np.ndarray, np.ndarray]:
    c1, c2 = parent_1.copy(), parent_2.copy() # children are copies of parents by default 

    if np.random.uniform(0, 1) < p_c: # typically 0.6 <= p_c <= 0.9 
        # select crossover point that is not on the end of the string 
        crossover_pt: int = np.random.randint(1, len(parent_1)-2)

        # exchange children's tails 
        c1 = np.concatenate((parent_1[:crossover_pt], parent_2[crossover_pt:]))
        c2 = np.concatenate((parent_2[:crossover_pt], parent_1[crossover_pt:]))
    return c1, c2



def mutation(bitstrings: np.ndarray, p_m: int | float):
    bitstring_size = len(bitstrings)
    for i in range(bitstring_size):
        if np.random.rand() < p_m:
            bitstrings[i] = 1 - bitstrings[i]








pop_size: int = 10

population = np.random.choice(
    a=2,
    size=pop_size,
    replace=True
)

num_generations:int = 100
for gen in range(num_generations):
    scores = evaluate_population_fitness(population)







