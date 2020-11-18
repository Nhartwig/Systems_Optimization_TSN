import numpy as np
import random
import time
from worst_case_delay import worst_case_delay


def simulated_annealing(tsn, startTemp=1000, coolFactor=1, cutoff_time=900):
    """
    Runs simulated annealing algorithm on the given network with given params.
    :param tsn:
    :param startTemp:
    :param coolFactor:
    :param cutoff_time:
    :returns: Returns output in the following format: (status, runtime, cost, seed)
    """
    # T = 1000  # Set
    # r = 0.03  # Set t declining factor
    start_time = time.time()

    T = startTemp
    r = coolFactor
    i = 0
    print("\n")

    worst_case_delay(tsn)
    cost0 = tsn.linksCost()
    tsn.save_Solution(cost0)

    while T > 1:  # Set loops
        T = T * (1 - r)

        worst_case_delay(tsn)
        cost0 = tsn.linksCost()

        i += 1
        if not i % 1:
            print("iteration i ", 100 * i, "cost = ", round(cost0, 1))

        for j in range(100):
            if time.time()-start_time >= cutoff_time:
                if not cost0:
                    cost = cost1
                else:
                    cost = cost0
                return("TIMEOUT", cutoff_time, cost, -1)
            # exchange two random tasks from two random cores and get a new neighbour solution
            s1 = random.choice(tsn.streams)  # pick a random stream
            if s1.routes:
                r1, r2 = s1.random_exchange(s1)  # From random stream s1 exchange 2 routes from solution and possible routes

            # Get the new cost
            cost1 = tsn.linksCost()

            if cost1 < cost0:
                cost0 = cost1
                tsn.save_Solution(cost0)
            else:
                x = np.random.uniform()

                if x < np.exp((cost0 - cost1) / T):
                    cost0 = cost1
                elif s1.routes:  # change solution to previous state
                    s1.routes.remove(r2)
                    s1.routes.append(r1)

                    s1.solution_routes.remove(r1)
                    s1.solution_routes.append(r2)

    cost0 = tsn.load_Best_Solution()
    runtime = time.time() - start_time
    # check the memory for the best solution.
    #print("total iterations = ", i * 100, "cost = ", round(cost0, 4))
    return("SUCCESS", runtime, cost0, -1)
