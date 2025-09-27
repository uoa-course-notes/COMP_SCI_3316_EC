class Crossover:
    def __init__(self, crossover_rate: float | int):
        self.crossover_rate = crossover_rate

    def perform_crossover(self, parent1, parent2):
        import random
        if random.random() < self.crossover_rate:
            point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        else:
            return parent1, parent2