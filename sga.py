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
    return random.choices(population, k=len(population))

def shuffle_mating_pool(mating_pool):
    # Shuffle the mating pool
    random.shuffle(mating_pool)
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






if __name__ == "__main__":
    print("This is the main module.")# sga.py