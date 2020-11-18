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
import datetime
import argparse
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


def findStreamsRoutes(tsn, G):
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

# def parsing_input(args):
#     folderPath = "../test_cases/"
#
#     if not args:
#         args.append("../test_cases/TC5_large1.xml")
#         filename = folderPath + args[0]
#     else:
#         filename = folderPath + args[0]
#
#     if os.path.exists(filename):
#         print("exists")
#         return filename
#     else:
#         sys.exit("\33[91mWrong file argument enter one of these: \33[93m \nTC0_example.xml \nTC1_check_red.xml \nTC2_check_bw.xml  \nTC3_medium.xml \nTC3_extended.xml  \nTC5_large1.xml \nTC6_large2.xml \nTC7_huge.xml \33[0m")
#     return filename
#
# filename = parsing_input(sys.argv[1:])

def check_input_temp(x):
    num = float(x)
    if num<0:
        raise ValueError('negative start temperatures not allowed')
    return num

def check_input_cooling(x):
    num = float(x)
    if (num<=0) or (num>=1):
        raise ValueError('cooling factor must be in range 0 to 1 (exclusive)')
    return num

def run_evaluation(filename, cutoff_time, seed, coolFactor, startTemp):
    # not sure if we need to use seed
    tsn = TSN(filename)
    G, N = createGraph(tsn)
    findStreamsRoutes(tsn, G)
    printStreamRoutes(tsn)
    generateGraphImage(N)
    return simulated_annealing(tsn, startTemp, coolFactor, cutoff_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # choices= ['../test_cases/TC3_medium.xml'
    # ,'../test_cases/TC3_extended.xml'
    # ,'../test_cases/TC1_check_red.xml'
    # ,'../test_cases/TC0_example.xml'
    # ,'../test_cases/TC5_large1.xml'
    # ,'../test_cases/TC7_huge.xml'
    # ,'../test_cases/TCX0_multicast.xml'],
    parser.add_argument('filename', action='store', default='../test_cases/TC5_large1.xml', help = 'a filename for the problem instance')
    parser.add_argument('-startTemp', action='store', default=1000, type=check_input_temp, help = 'initial temperature for SA algo')
    parser.add_argument('-coolFactor', action='store', default=0.03, type=check_input_cooling,help = 'the temperature decline factor of the algo')

    args = parser.parse_args()
    filename = args.filename
    startTemp = float(args.startTemp)
    coolFactor = float(args.coolFactor)

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

    findStreamsRoutes(tsn, G)  # we find for each stream the possible routes and create our initial solution

    printStreamRoutes(tsn)

    generateGraphImage(N)  # generate graph image with input only the devices names

    start_time = datetime.datetime.now().strftime("%d %B %Y %X")
    (status, runtime, cost, seed) = simulated_annealing(tsn, startTemp, coolFactor)  # run simulated annealing algorithm
    print("Cost:", cost, "Runtime (seconds): ", runtime)

    # printSolution(tsn)  # print solution

    outputSolutionXML(tsn, filename, start_time)  # output results to xml file

    worst_case_delay(tsn)

    for device in tsn.devices:
        if device.type == "Switch":
            print(" \033[0m", device.name," cycle time = ", round(device.cycleTime, 3))

    for s in tsn.streams:
        print(s.id, " route lenght = ", math.ceil(len(s.solution_links)/s.rl), "worst cycle delay = ", round(tsn.stream_wct(s), 3))
