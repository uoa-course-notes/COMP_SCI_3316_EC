import numpy as np
import random 
from ioh import get_problem, ProblemClass, logger
from ioh import Experiment


class RandomSearch:
    def __init__(self, budget):
        # we need to rerun all dynamic variables if we want to run the same algorithm again
        self.budget = budget


        # a parameter static over the course of an optimization run of an algorithm
        self.algorithm_id = np.random.randint(100)

        # a dynamic parameter updated by the algorithm 
        self.a_tracked_parameter = None 

    def __call__(self, func):
        self.f_opt = float(np.inf)
        self.x_opt = None
        for i in range(self.budget):
            x = np.random.uniform(func.bounds.lb, func.bounds.ub)
            # updating the tracked parameter
            self.a_tracked_parameter = i ** 10 
            f = func(x)
            if f < self.f_opt:
                self.f_opt = f 
                self.x_opt = x 


            return self.f_opt, self.x_opt 


    @property
    def a_property(self):
        return np.random.randint(100)
    
    def reset(self):
        self.algorithm_id = np.random.randint(100)

        
# exp = Experiment(
#     RandomSearch(10),                   # instance of optimization algorithm
#     [1],                                # list of problem id's
#     [1, 2],                             # list of problem instances
#     [5],                                # list of problem dimensions
#     problem_class = ProblemClass.BBOB,  # the problem type, function ids should correspond to problems of this type
#     njobs = 1,                          # the number of parrellel jobs for running this experiment
#     reps = 2,                           # the number of repetitions for each (id x instance x dim)
#     logged_attributes = [               # list of the tracked variables, must be available on the algorithm instance (RandomSearch)
#         "a_property",
#         "a_tracked_parameter"
#     ]
# )

# Full example 

algorithm = RandomSearch(budget=10)
print(f"Algorithm ID = {algorithm.algorithm_id}")
print(f"Property = {algorithm.a_property}")

l3 = logger.Analyzer(folder_name='temp3')

# track variables static over the course of an algorithm run 
l3.add_run_attributes(algorithm, ["algorithm_id"])


# Track dynamic variables, updated during the run of an algorithm
l3.watch(algorithm, ["a_property", "a_tracked_parameter"])


# attach a problem to the logger 
p2 = get_problem(2, 2, 5)
p2.attach_logger(l3)



runs = 10 
for run in range(runs):
    algorithm(p2) # run the algorithm on the problem
    p2.reset() # reset the problem for the next run
    algorithm.reset() # reset the algorithm for the next run