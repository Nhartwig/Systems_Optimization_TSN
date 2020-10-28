import numpy as np
import random


def simulated_annealing(tsn):
    T = 1000  # Set
    r = 0.003  # Set t declining factor

    i = 0

    print("\n")

    while T > 1:  # Set loops
        T = T * (1 - r)
        cost0 = tsn.linksCost()

        i += 1
        if not i % 10:
            print("iteration i ", 100 * i, "cost = ", round(cost0, 4))
        for j in range(100):
            # exchange two random tasks from two random cores and get a new neighbour solution

            s1 = random.choice(tsn.streams)

            r1, r2 = s1.random_exchange()

            tries = 0

            # while r1 == r2 and tries < 10:
            #     r1, r2 = s1.random_exchange()
            #     tries +=1
            if tries < 10:
                s1.solution_routes.remove(r2)
                s1.solution_routes.append(r1)

            # Get the new cost
            cost1 = tsn.linksCost()

            if cost1 < cost0:
                cost0 = cost1
            else:
                x = np.random.uniform()
                if x < np.exp((cost0 - cost1) / T):
                    cost0 = cost1
                else:  # change solution to previous state
                    s1.solution_routes.remove(r1)
                    s1.solution_routes.append(r2)

    print("total iterations = ", i * 100, "cost = ", round(cost0, 4))


