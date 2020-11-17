##
#    @mainpage Systems Optimization exercise
#
#    @authors                 Basian Lesi
#    @authors                 Olga Athanasopoulou
#    @authors                 Nathaniel Stephen Frost Hartwig
#    @authors                 Matej Poljuha

import networkx as nx
import sys
import os
import math
from matplotlib import pyplot as plt
from inputData import *
from simulated_Annealing import *
from output_xml import *
from worst_case_delay import *



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
    for stream in tsn.streams:
        stream.findRoutes(G)
        stream.initial_solution()


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
    pos = nx.spectral_layout(graph)
    nx.draw_networkx(graph, arrows=True, font_size=6, pos = pos, font_color = 'w', arrowsize=6)
    plt.savefig("../images/Graph_Image.png", format="PNG")
    plt.clf()


def printSolution(tsn):
    for s in tsn.streams:
        s.printRouteLinks(tsn)

def parsing_input(args):
    folderPath = "../test_cases/"

    if not args:
        args.append("../test_cases/TC5_large1.xml")
        filename = folderPath + args[0]
    else:
        filename = folderPath + args[0]
    
    if os.path.exists(filename):
        print("exists")
        return filename
    else:
        sys.exit("\33[91mWrong file argument enter one of these: \33[93m \nTC0_example.xml \nTC1_check_red.xml \nTC2_check_bw.xml  \nTC3_medium.xml \nTC3_extended.xml  \nTC5_large1.xml \nTC6_large2.xml \nTC7_huge.xml \33[0m")
    return filename


filename = parsing_input(sys.argv[1:])

# filename = '../test_cases/TC3_medium.xml'
# filename = '../test_cases/TC3_extended.xml'
# filename = '../test_cases/TC1_check_red.xml'
# filename = '../test_cases/TC0_example.xml'
# filename = '../test_cases/TC5_large1.xml'
# filename = '../test_cases/TC7_huge.xml'
# filename = '../test_cases/TCX0_multicast.xml'

tsn = TSN(filename)  # create tsn object

G, N = createGraph(tsn)  # createGraph(tsn) returns two graphs, one with device objects as nodes
# and one with device objects names as nodes

findStreamsRoutes(tsn)  # we find for each stream the possible routes and create our initial solution

printStreamRoutes(tsn)

generateGraphImage(N)  # generate graph image with input only the devices names

simulated_annealing(tsn)  # run simulated annealing algorithm

printSolution(tsn)  # print solution

outputSolutionXML(tsn, filename)  # output results to xml file

worst_case_delay(tsn)

for device in tsn.devices:
    if device.type == "Switch":
        print(" \033[0m", device.name," cycle time = ", round(device.cycleTime, 3))

for s in tsn.streams:
    print(s.id, " route lenght = ", math.ceil(len(s.solution_links)/s.rl), "worst cycle delay = ", round(tsn.stream_wct(s), 3))
