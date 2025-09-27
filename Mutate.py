class Mutation:
    def __init__(self, mutation_type, target, value):
        self.mutation_type = mutation_type  # e.g., 'insert', 'delete', 'modify'
        self.target = target                  # e.g., the location or element to mutate
        self.value = value                    # e.g., the new value for modification or insertion

    def apply(self, data_structure):
        if self.mutation_type == 'insert':
            data_structure.insert(self.target, self.value)
        elif self.mutation_type == 'delete':
            del data_structure[self.target]
        elif self.mutation_type == 'modify':
            data_structure[self.target] = self.value
        else:
            raise ValueError(f"Unknown mutation type: {self.mutation_type}")

    def __repr__(self):
        return f"Mutation(type={self.mutation_type}, target={self.target}, value={self.value})"