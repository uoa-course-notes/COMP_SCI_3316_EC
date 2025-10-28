from .algorithm_interface import Algorithm
import ioh 
import numpy as np


class SingleObjectiveEA(Algorithm):
    '''
    Population-based Fast Genetic Algorithm with power-law mutation (β=1.5).
    Designed for monotone submodular optimization problems with uniform constraints.
    Includes constraint repair and diversity maintenance mechanisms.
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

    # ==================== CONSTRAINT REPAIR ====================
    
    def repair_solution(self, individual: np.ndarray, func) -> np.ndarray:
        '''
        Repair infeasible solution by greedily removing nodes.
        Removes nodes until solution becomes feasible (positive fitness).
        '''
        solution = individual.copy()
        fitness = func(solution.tolist())
        
        # If already feasible, return as is
        if fitness >= 0:
            return solution
        
        # Greedily remove nodes while infeasible
        max_repairs = 10  # Limit repair iterations to avoid excessive evaluations
        repairs = 0
        
        while fitness < 0 and func.state.evaluations < self.budget and repairs < max_repairs:
            selected_indices = np.where(solution == 1)[0]
            
            if len(selected_indices) == 0:
                break  # No nodes to remove
            
            # Simple repair: randomly remove one node
            # (Could be enhanced with marginal loss calculation)
            remove_idx = np.random.choice(selected_indices)
            solution[remove_idx] = 0
            
            fitness = func(solution.tolist())
            repairs += 1
        
        return solution

    # ==================== SELECTION ====================
    
    def tournament_select(self, population: list, fitnesses: list) -> np.ndarray:
        '''
        Select one individual via k-tournament selection.
        Promotes better individuals while maintaining diversity.
        '''
        tournament_indices = np.random.choice(
            len(population), 
            size=min(self.tournament_size, len(population)), 
            replace=False
        )
        tournament_fitnesses = [fitnesses[i] for i in tournament_indices]
        winner_idx = tournament_indices[np.argmax(tournament_fitnesses)]
        return population[winner_idx].copy()

    # ==================== DIVERSITY MAINTENANCE ====================
    
    def calculate_diversity(self, population: list) -> float:
        '''
        Calculate population diversity using average Hamming distance.
        Higher values indicate more diverse population.
        '''
        if len(population) < 2:
            return 0.0
        
        total_distance = 0.0
        comparisons = 0
        
        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                # Hamming distance: count differing bits
                distance = np.sum(population[i] != population[j])
                total_distance += distance
                comparisons += 1
        
        return total_distance / comparisons if comparisons > 0 else 0.0

    def diversity_selection(self, population: list, fitnesses: list, 
                            target_size: int) -> tuple:
        '''
        Select individuals balancing fitness and diversity.
        Uses fitness-based selection with diversity penalty for similar individuals.
        '''
        if len(population) <= target_size:
            return population, fitnesses
        
        selected_pop = []
        selected_fit = []
        
        # Always keep the best individual (elitism)
        best_idx = np.argmax(fitnesses)
        selected_pop.append(population[best_idx].copy())
        selected_fit.append(fitnesses[best_idx])
        
        remaining_indices = list(range(len(population)))
        remaining_indices.remove(best_idx)
        
        # Select remaining individuals with diversity consideration
        while len(selected_pop) < target_size and remaining_indices:
            best_score = -np.inf
            best_idx_in_remaining = -1
            
            for idx in remaining_indices:
                # Calculate diversity score: min distance to selected individuals
                min_distance = min([
                    np.sum(population[idx] != sel) 
                    for sel in selected_pop
                ])
                
                # Combined score: fitness + diversity bonus
                diversity_bonus = min_distance / len(population[idx]) * 0.1
                score = fitnesses[idx] + diversity_bonus
                
                if score > best_score:
                    best_score = score
                    best_idx_in_remaining = idx
            
            if best_idx_in_remaining != -1:
                selected_pop.append(population[best_idx_in_remaining].copy())
                selected_fit.append(fitnesses[best_idx_in_remaining])
                remaining_indices.remove(best_idx_in_remaining)
            else:
                break
        
        return selected_pop, selected_fit

    # ==================== MAIN ALGORITHM ====================
    
    def run_optimization_loop(self, func: ioh.problem.GraphProblem):
        n = func.meta_data.n_variables
        
        # Initialize power-law distribution
        self.power_law_distribution = self.compute_power_law_distribution(n)
        
        # Initialize population randomly
        population = [np.random.randint(0, 2, size=n) for _ in range(self.population_size)]
        
        # Evaluate and repair initial population
        fitnesses = []
        for i in range(self.population_size):
            fitness = func(population[i].tolist())
            if fitness < 0:
                population[i] = self.repair_solution(population[i], func)
                fitness = func(population[i].tolist())
            fitnesses.append(fitness)
        
        generation = 0
        
        # Main evolutionary loop
        while func.state.evaluations < self.budget:
            # Early termination if optimum found
            if func.state.optimum_found:
                break
            
            # Generate offspring population
            offspring_population = []
            offspring_fitnesses = []
            
            for _ in range(self.population_size):
                if func.state.evaluations >= self.budget:
                    break
                
                # Parent selection via tournament
                parent = self.tournament_select(population, fitnesses)
                
                # Generate offspring via power-law mutation
                offspring = self.mutate(parent, n)
                
                # Evaluate offspring
                offspring_fitness = func(offspring.tolist())
                
                # Repair if infeasible
                if offspring_fitness < 0:
                    offspring = self.repair_solution(offspring, func)
                    if func.state.evaluations < self.budget:
                        offspring_fitness = func(offspring.tolist())
                
                offspring_population.append(offspring)
                offspring_fitnesses.append(offspring_fitness)
            
            # Combine parent and offspring populations
            combined_population = population + offspring_population
            combined_fitnesses = fitnesses + offspring_fitnesses
            
            # Diversity-aware survival selection
            population, fitnesses = self.diversity_selection(
                combined_population, 
                combined_fitnesses, 
                self.population_size
            )
            
            generation += 1

    def __call__(self, func: ioh.problem.PBO):
        self.run_optimization_loop(func)