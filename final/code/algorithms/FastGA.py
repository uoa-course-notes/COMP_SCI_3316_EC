from .algorithm_interface import Algorithm
import ioh 
import numpy as np


class FastGA(Algorithm):
    '''
    Fast Genetic Algorithm with power-law mutation (β=1.5).
    Based on the theoretical work showing power-law mutation is efficient 
    for submodular optimization problems.
    '''
    def __init__(self, budget: int, population_size: int = 2, beta: float = 1.5):
        super().__init__(budget, name="Fast GA", algorithm_info="(1+1) Fast Genetic Algorithm with power-law mutation.")
        self.population_size = population_size  # Typically (1+1), so mu=1, lambda=1
        self.budget = budget 
        self.beta = beta  # Power-law exponent (default 1.5)
        self.power_law_distribution = None

    def compute_power_law_distribution(self, n: int) -> np.ndarray:
        '''
        Computes the power-law distribution for mutation strength sampling.
        P(k) ∝ k^(-beta) for k = 1, 2, ..., n/2
        '''
        distribution = np.zeros(n + 1)
        
        # Compute normalization constant C
        C = 0.0
        for i in range(1, n // 2 + 1):
            C += i ** (-self.beta)
        
        # Compute probability for each mutation strength
        for i in range(1, n + 1):
            if i <= n // 2:
                distribution[i] = (1.0 / C) * (i ** (-self.beta))
            else:
                distribution[i] = 0.0
        
        distribution[0] = 0.0  # Never flip 0 bits
        
        return distribution

    def sample_mutation_strength(self, n: int) -> int:
        '''
        Sample the number of bits to flip from the power-law distribution.
        '''
        if self.power_law_distribution is None:
            self.power_law_distribution = self.compute_power_law_distribution(n)
        
        # Sample from power-law distribution
        k = np.random.choice(n + 1, p=self.power_law_distribution)
        
        # Ensure at least 1 bit is flipped
        if k == 0:
            k = 1
            
        return k

    def mutate(self, individual: np.ndarray, n: int) -> np.ndarray:
        '''
        Power-law mutation: sample mutation strength from power-law distribution,
        then flip that many random bits.
        '''
        offspring = individual.copy()
        
        # Sample number of bits to flip from power-law distribution
        num_flips = self.sample_mutation_strength(n)
        
        # Randomly select which bits to flip
        flip_indices = np.random.choice(n, size=num_flips, replace=False)
        
        # Flip the selected bits
        offspring[flip_indices] = 1 - offspring[flip_indices]
        
        return offspring

    def __call__(self, func: ioh.problem.PBO):
        n = func.meta_data.n_variables
        
        # Initialize power-law distribution for this problem dimension
        self.power_law_distribution = self.compute_power_law_distribution(n)
        
        # Initialize random solution (parent)
        current = np.random.randint(0, 2, size=n)
        current_fitness = func(current.tolist())
        
        # (1+1) Fast GA: maintain one parent, generate one offspring per iteration
        while func.state.evaluations < self.budget:
            # Early termination if optimum found
            if func.state.optimum_found:
                break
            
            # Generate offspring using power-law mutation
            offspring = self.mutate(current, n)
            offspring_fitness = func(offspring.tolist())
            
            # Elitist selection: keep offspring if it's at least as good
            if offspring_fitness >= current_fitness:
                current = offspring
                current_fitness = offspring_fitness