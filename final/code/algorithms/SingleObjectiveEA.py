from .algorithm_interface import Algorithm
import ioh 
import numpy as np


class SingleObjectiveEA(Algorithm):
    '''
    Population-based Fast GA for monotone submodular graph problems.
    Uses evaluation feedback to handle constraints, not structural assumptions.
    '''
    def __init__(self, budget: int, population_size: int = 20, beta: float = 1.5, 
                 tournament_size: int = 3):
        super().__init__(budget, name="Fast GA", 
                        algorithm_info=f"Population-based Fast GA (pop={population_size}, β={beta})")
        self.population_size = population_size
        self.budget = budget 
        self.beta = beta
        self.tournament_size = tournament_size
        self.power_law_distribution = None

    # ==================== POWER-LAW MUTATION ====================
    
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
        Power-law mutation: sample mutation strength and flip random bits.
        '''
        offspring = individual.copy()
        
        # Sample number of bits to flip
        num_flips = self.sample_mutation_strength(n)
        
        # Randomly select which bits to flip
        flip_indices = np.random.choice(n, size=num_flips, replace=False)
        
        # Flip the selected bits
        offspring[flip_indices] = 1 - offspring[flip_indices]
        
        return offspring

    # ==================== CONSTRAINT REPAIR ====================
    
    def repair_by_removal(self, individual: np.ndarray, func, max_attempts: int = 5) -> tuple:
        '''
        Repair infeasible solution by removing random 1s.
        Returns (repaired_solution, fitness, num_repairs_used)
        '''
        solution = individual.copy()
        fitness = func(solution.tolist())
        repairs_used = 0
        
        if fitness >= 0:
            return solution, fitness, 0
        
        # Try removing nodes until feasible or max attempts reached
        for attempt in range(max_attempts):
            if func.state.evaluations >= self.budget or fitness >= 0:
                break
            
            ones_positions = np.where(solution == 1)[0]
            
            if len(ones_positions) == 0:
                break  # No more nodes to remove
            
            # Remove 10-20% of selected nodes
            num_to_remove = max(1, len(ones_positions) // 10)
            remove_positions = np.random.choice(ones_positions, size=num_to_remove, replace=False)
            solution[remove_positions] = 0
            
            fitness = func(solution.tolist())
            repairs_used += 1
        
        return solution, fitness, repairs_used

    # ==================== SELECTION ====================
    
    def tournament_select(self, population: list, fitnesses: list) -> np.ndarray:
        '''
        Tournament selection with Deb's feasibility rules:
        - Feasible (>=0) always beats infeasible (<0)
        - Among feasible: higher fitness wins
        - Among infeasible: higher fitness wins (less violation)
        '''
        tournament_indices = np.random.choice(
            len(population), 
            size=min(self.tournament_size, len(population)), 
            replace=False
        )
        
        # Get fitnesses and separate by feasibility
        tournament_fits = [fitnesses[i] for i in tournament_indices]
        feasible_indices = [i for i, fit in enumerate(tournament_fits) if fit >= 0]
        
        if feasible_indices:
            # At least one feasible: pick best feasible
            best_local = max(feasible_indices, key=lambda i: tournament_fits[i])
        else:
            # All infeasible: pick least infeasible
            best_local = np.argmax(tournament_fits)
        
        winner_idx = tournament_indices[best_local]
        return population[winner_idx].copy()

    # ==================== MAIN ALGORITHM ====================
    
    def __call__(self, func: ioh.problem.PBO):
        n = func.meta_data.n_variables
        
        # Initialize power-law distribution
        self.power_law_distribution = self.compute_power_law_distribution(n)
        
        # Initialize population with SPARSE solutions (more likely to be feasible)
        population = []
        for _ in range(self.population_size):
            individual = np.zeros(n, dtype=int)
            # Start with 5-10% of nodes selected
            num_ones = np.random.randint(max(1, n // 20), max(2, n // 10))
            ones_positions = np.random.choice(n, size=num_ones, replace=False)
            individual[ones_positions] = 1
            population.append(individual)
        
        # Evaluate and repair initial population
        fitnesses = []
        for i in range(self.population_size):
            if func.state.evaluations >= self.budget:
                break
            
            # Evaluate
            fitness = func(population[i].tolist())
            
            # Repair if infeasible
            if fitness < 0:
                population[i], fitness, _ = self.repair_by_removal(population[i], func)
            
            fitnesses.append(fitness)
        
        generation = 0
        no_feasible_count = 0
        
        # Main evolutionary loop
        while func.state.evaluations < self.budget:
            if func.state.optimum_found:
                break
            
            # Track feasibility
            num_feasible = sum(1 for f in fitnesses if f >= 0)
            
            # Generate offspring
            offspring_population = []
            offspring_fitnesses = []
            
            for _ in range(self.population_size):
                if func.state.evaluations >= self.budget:
                    break
                
                # Select parent (prefers feasible solutions)
                parent = self.tournament_select(population, fitnesses)
                
                # Mutate
                offspring = self.mutate(parent, n)
                
                # Evaluate
                offspring_fitness = func(offspring.tolist())
                
                # Repair if infeasible (but only sometimes to save evaluations)
                if offspring_fitness < 0:
                    # Repair with probability based on population feasibility
                    repair_prob = 0.5 if num_feasible < self.population_size // 2 else 0.2
                    
                    if np.random.rand() < repair_prob and func.state.evaluations < self.budget - 50:
                        offspring, offspring_fitness, _ = self.repair_by_removal(offspring, func, max_attempts=3)
                
                offspring_population.append(offspring)
                offspring_fitnesses.append(offspring_fitness)
            
            # Survival selection: keep best from parents + offspring
            combined_pop = population + offspring_population
            combined_fit = fitnesses + offspring_fitnesses
            
            # Sort by fitness (feasible solutions first, then by fitness value)
            def sort_key(idx):
                f = combined_fit[idx]
                if f >= 0:
                    return (1, f)  # Feasible: priority 1, sort by fitness
                else:
                    return (0, f)  # Infeasible: priority 0, sort by least violation
            
            sorted_indices = sorted(range(len(combined_pop)), key=sort_key, reverse=True)
            
            # Keep top population_size
            population = [combined_pop[i] for i in sorted_indices[:self.population_size]]
            fitnesses = [combined_fit[i] for i in sorted_indices[:self.population_size]]
            
            generation += 1