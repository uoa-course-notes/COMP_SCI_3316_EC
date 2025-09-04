# from ioh import problem
from ioh import get_problem, ProblemClass, logger 
import numpy as np 


np.random.seed(42)
def random_search(func, budget = 10):
    for i in range(budget):
        x = np.random.uniform(func.bounds.lb, func.bounds.ub)
        func(x)

# help(problem)



# create a default logger which writes to folder 'temp'
folder_name = 'temp'
l = logger.Analyzer(folder_name=folder_name)

f = get_problem(1, 1, 5, ProblemClass.PBO)
print(f"Problem type = {f}")

# run the algorithm and store data
random_search(f)

# this can then be attached to the problem
# f.attach_logger(l)




# f = get_problem(1, 1, 5, ProblemClass.PBO)
# print(f"meta_data = {f.meta_data}")
# print(f"state = {f.state}")
# print(f"Evaluated = {f([0,0,0,0,0])}")

# f.reset()



# Walkthrough from tutorial below:
# https://iohprofiler.github.io/IOHexperimenter/python