import xml.etree.ElementTree as ET
import networkx as nx
import numpy as np
import random


class TSN:
    ## TSN (Time Nensitive Network) initializer.
    #
    #    @param devices             List with devices objects.
    #    @param streams             List with stream objects.
    #    @param links               List with links objects.
    #
    #    @return   An instance of the TSN class initializer with devices, streams and links lists of objects.

    def __init__(self):

        tree = ET.parse('../test_cases/TC3_medium.xml')
        # tree = ET.parse('../test_cases/TC0_example.xml')

        self.devices = []
        self.streams = []
        self.links = []
        self.createDeviceObjects(tree.getroot())
        self.createLinkObjects(tree.getroot())
        self.createStreamObjects(tree.getroot())

    ## Creates the Device Objects
    #
    #    @param root      The tree root of the xml input data file.
    #
    #    @return No return.
    def createDeviceObjects(self, root):
        for d in root.iter('device'):
            dev_id = len(self.devices)
            dev_name = d.get('name')
            dev_type = d.get('type')
            self.devices.append(Device(dev_id, dev_name, dev_type))

    ## Creates the link Objects
    #
    #    @param root      The tree root of the xml input data file.
    #
    #    @return No return.
    def createLinkObjects(self, root):
        for lin in root.iter('link'):
            src = lin.get('src')
            dest = lin.get('dest')
            speed = float(lin.get('speed'))

            #For each link in the xml file, find the source and destination device objects.
            for dev in self.devices:
                if src == dev.name:
                    source_device = dev
                if dest == dev.name:
                    dest_device = dev
            source_device.vertices.append(dest_device)
            self.links.append(Link(source_device,
                                   dest_device,
                                   speed))

    ## Creates the Stream Objects
    #
    #    @param root      The tree root of the xml input data file.
    #
    #    @return No return.
    def createStreamObjects(self, root):
        for s in root.iter('stream'):
            id = s.get('id')
            rl = int(s.get('rl'))
            src = s.get('src')
            dest = s.get('dest')
            size = int(s.get('size'))
            period = int(s.get('period'))
            deadline = s.get('deadline')

            for dev in self.devices:
                if src == dev.name:
                    source_device = dev
                if dest == dev.name:
                    dest_device = dev

            self.streams.append(Stream(id,
                                       source_device,
                                       dest_device,
                                       size, period,
                                       deadline, rl))

    ## Carculates the Cost for each link
    #
    # @return The cost depending on the bandwidth used, more bandwidth used the higher the cost value.
    def linksCost(self):
        cost = 0
        for s in self.streams:
            cost += s.stream_cost(self)

        self.resetLinkBandwidth()
        return cost

    ## Resets links used bandwidth
    #
    #   Reset the links bandwidth after the cost calculation.
    #   Every solution starts with used_bandwidth at zero value.
    #
    #    @return No return.
    def resetLinkBandwidth(self):
        for link in self.links:
            link.used_bandwidth = 0


class Device:

    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type
        self.vertices = []


class Link:

    def __init__(self, source_device, dest_device, speed):
        self.src = source_device
        self.dest = dest_device
        self.bandwidth = speed * 8
        self.used_bandwidth = 0


class Stream:

    def __init__(self, id, source_device, dest_device, size, period, deadline, rl):
        self.id = id
        self.rl = rl
        self.src = source_device
        self.dest = dest_device
        self.size = size
        self.period = period
        self.deadline = deadline
        self.stream_bandwidth = self.size / self.period
        self.routes = []
        self.solution_routes = []
        self.solution_links = []

    def findRoutes(self, graph):
        route = nx.all_simple_paths(graph, self.src, self.dest, cutoff=7)
        for r in route:
            self.routes.append(r)

    def initial_solution(self):
        for i in range(self.rl):
            self.solution_routes.append(self.routes[i])

    def solution_Links(self, tsn):
        self.solution_links.clear()
        for route in self.solution_routes:
            for i in range(0, len(route) - 1):
                src_device = route[i]
                dest_device = route[i + 1]
                for link in tsn.links:
                    if (link.src == src_device) and (link.dest == dest_device):
                        self.solution_links.append(link)
                        # print("link src, dest = (", link.src.name, " ,", link.dest.name, " )")

    def stream_cost(self, tsn):
        self.solution_Links(tsn)
        cost = 0;
        for link in self.solution_links:
            link.used_bandwidth += self.stream_bandwidth
            cost += link.used_bandwidth
            if link.used_bandwidth > link.bandwidth:
                cost = cost * 10
        return cost

    def random_exchange(self):
        r1 = random.choice(self.routes)
        r2 = random.choice(self.solution_routes)
        # print("r1 r2 =====", r1[2].name, ", ", r2[2].name)
        return r1, r2

    def printRouteLinks(self, tsn):
        self.solution_links.clear()
        print(self.id)
        k = 1
        for route in self.solution_routes:
            print("route ", k)
            k += 1
            for i in range(0, len(route) - 1):
                src_device = route[i]
                dest_device = route[i + 1]
                for link in tsn.links:
                    if (link.src == src_device) and (link.dest == dest_device):
                        self.solution_links.append(link)
                        print("link src, dest = (", link.src.name, " ,", link.dest.name, " )")
