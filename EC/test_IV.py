# run_inner_all.py
# Runs the Inner operator across multiple TSPlib instances and writes
# stats to results/inner_over.txt: shortest, median, minimum, std.

import time, random, os
from TSPLib import np
from files import Output  # not required for this file, but fine to keep if you use elsewhere
# If your Inner class is in a different module, adjust this import accordingly:
from Inver_over import Inner

INSTANCES = [
    "EIL51","EIL76","EIL101","ST70",
    "KROA100","KROC100","KROD100","LIN105",
    "PCB442","PR2392"
]

POP_SIZE  = 30
MAX_ITERS = 1000
RUNS      = 20
P_VALUE   = 0.01

RESULTS_PATH = "results/inner_over.txt"

def make_filename(name: str) -> str:
    return f"{name.lower()}.tsp"

def build_inner(pop_size: int, tsp_file: str, p_value: float, max_iters: int):
    """Construct Inner regardless of whether it accepts max_iters or not."""
    try:
        return Inner(size=pop_size, filename=tsp_file, p_value=p_value, max_iters=max_iters)
    except TypeError:
        return Inner(size=pop_size, filename=tsp_file, p_value=p_value)


def write_stats(instance: str, values: np.ndarray):
    """Append requested stats to results/inner_over.txt."""
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    shortest = int(np.min(values))               # requested: 'shortest'
    median   = float(np.median(values))          # requested: 'median'
    minimum  = int(np.min(values))               # requested: 'minimum' (same as shortest)
    std      = float(np.std(values))

    with open(RESULTS_PATH, "a") as f:
        f.write(f"{instance}\n")
        f.write(f"  shortest: {shortest}\n")
        f.write(f"  median:   {median:.2f}\n")
        f.write(f"  minimum:  {minimum}\n")
        f.write(f"  std:      {std:.2f}\n\n")

def run_instance(instance: str):
    fn = make_filename(instance)
    lengths = np.zeros(RUNS, dtype=int)

    print(f"\n=== {instance} | pop={POP_SIZE} | iters={MAX_ITERS} | runs={RUNS} | p={P_VALUE} ===")
    for i in range(RUNS):
        seed = 42 + i
        random.seed(seed)
        np.random.seed(seed)

        t0 = time.time()
        inner = build_inner(POP_SIZE, fn, P_VALUE, MAX_ITERS)
        best = int(inner.getBest()[0])
        dt = time.time() - t0

        lengths[i] = best
        print(f"  run {i+1:2d}: best={best}  time={dt:.2f}s")

    # Write exactly the requested stats
    write_stats(instance, lengths)

def main():
    # clear/initialize output file header
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        f.write("Inner Over Results (pop=50, iters=20000, runs=30)\n\n")

    for inst in INSTANCES:
        run_instance(inst)

if __name__ == "__main__":
    main()