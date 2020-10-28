##
#    @mainpage Systems Optimization exercise
#
#    @authors                 Basian Lesi
#    @authors                 Olga Athanasopoulou
#    @authors                 Nathaniel Stephen Frost Hartwig
#    @authors                 Matej Poljuha

import networkx as nx
import matplotlib.pyplot as plt
from inputData import *
from simulated_Annealing import *


def createGraph(tsn_object):
    graph = nx.DiGraph()
    names = nx.DiGraph()

    for device in tsn_object.devices:
        graph.add_node(device)
        names.add_node(device.name)

    for link in tsn_object.links:
        graph.add_edge(link.src, link.dest)
        names.add_edge(link.src.name, link.dest.name)
    graph.edges()
    return graph, names


def findStreamsRoutes(tsn):
    for s in tsn.streams:
        s.findRoutes(G)
        s.initial_solution()


def printStreamRoutes(tsn):
    for stream in tsn.streams:
        print("\n\n", stream.id, " rl = ", stream.rl)
        i = 0
        for route in stream.routes:
            i = i + 1
            print("\n", i, " route")
            for r in route:
                print(r.name, end=" ")


def generateGraphImage(graph):
    plt.tight_layout()
    nx.draw_networkx(graph, arrows=True)
    plt.savefig("../images/Graph_Image.png", format="PNG")
    plt.clf()


def printSolution(tsn):
    for s in tsn.streams:
        s.printRouteLinks(tsn)


tsn = TSN()                 #create tsn object

G, N = createGraph(tsn)     #createGraph(tsn) returns two graphs, one with device objects as nodes
                            # and one with device objects names as nodes

findStreamsRoutes(tsn)      #we find for each stream the possible routes and create our initial solution

printStreamRoutes(tsn)

generateGraphImage(N)       #generate graph image with input only the devices names

simulated_annealing(tsn)    #run simulated annealing algorithm

printSolution(tsn)          #print solution