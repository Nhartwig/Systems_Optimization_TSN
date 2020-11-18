import xml.etree.ElementTree as ET
import networkx as nx
import random
import math


class TSN:
    ## TSN (Time Sensitive Network) initializer.
    #
    #    @param devices             List with devices objects.
    #    @param streams             List with stream objects.
    #    @param links               List with links objects.
    #
    #    @return   An instance of the TSN class initializer with devices, streams and links lists of objects.

    def __init__(self, filename="../test_cases/TC3_medium.xml"):

        tree = ET.parse(filename)

        self.devices = []
        self.streams = []
        self.links = []
        self.createDeviceObjects(tree.getroot())
        self.createLinkObjects(tree.getroot())
        self.createStreamObjects(tree.getroot())
        self.savedCost = 100000000  # initial cost

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

            # For each link in the xml file, find the source and destination device objects.
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

    ## Calculates the Cost for each link
    #
    # @return The cost (depending on the bandwidth used) multiplied by the Link similarity of critical streams, more bandwidth used the higher the cost value.
    def linksCost(self):
        cost = 0
        wct = 0
        for s in self.streams:
            cost += s.stream_cost(self)
            wct += self.stream_wct(s)

        self.resetLinkBandwidth()
        similarity = self.similarLinks()
        return cost + similarity + wct

    ## Calculates the similar links between the different routes for the critical streams
    #
    # @return A number that is proportional to how many similar links each stream has (the smaller the better)
    def similarLinks(self):
        similarity_links = 1
        for s in self.streams:
            if s.rl > 1:
                for i in range(0, len(s.solution_links) - 1):
                    link_1 = s.solution_links[i]
                    for j in range(i + 1, len(s.solution_links)):
                        link_2 = s.solution_links[j]
                        if link_1 == link_2:
                            similarity_links += 1
        return similarity_links


    def stream_wct(self, s):
        max = 0
        for l in s.solution_links:
            if l.src.type == "Switch":
                if l.src.cycleTime > max:
                    max = l.src.cycleTime 
        return max


    ## Resets links used bandwidth
    #
    #   Reset the links bandwidth after the cost calculation.
    #   Every solution starts with used_bandwidth at zero value.
    #
    #    @return No return.
    def resetLinkBandwidth(self):
        for link in self.links:
            link.used_bandwidth = 0

    def save_Solution(self, cost):
        if cost < self.savedCost:
            self.savedCost = cost
            for stream in self.streams:
                stream.saved_solution_routes = stream.solution_routes

    def load_Best_Solution(self):
        for stream in self.streams:
            stream.solution_routes = stream.saved_solution_routes
        return self.savedCost


class Device:

    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type
        self.vertices = []
        self.speed = 0
        self.egressPort = []        #contains the streams that are using the switch devices
        self.cycleTime  = 0
        
        


class Link:

    def __init__(self, source_device, dest_device, speed):
        self.src = source_device
        self.dest = dest_device
        self.bandwidth = speed * 8
        self.used_bandwidth = 0
        self.src.speed = speed * 8     #Mbit/s which is the bandwidth size of the link
        


class Stream:

    def __init__(self, id, source_device, dest_device, size, period, deadline, rl):
        self.id = id
        self.rl = rl
        self.src = source_device
        self.dest = dest_device
        self.size = size
        self.period = period
        self.deadline = deadline
        self.stream_bandwidth = 8 * self.size / self.period
        self.routes = []
        self.solution_routes = []
        self.saved_solution_routes = []
        self.solution_links = []
        self.priority = 0

    ## Find all the possible routes for the stream from its source to destination with maximum length of 'cutoff = 8' links
    #
    # @return has no return
    def findRoutes(self, graph):
        route = nx.all_simple_paths(graph, self.src, self.dest, cutoff=15)
        for r in route:
            self.routes.append(r)

    ## Initialising a random solution for the routes
    #
    #@return has no return
    def initial_solution(self):
        for i in range(self.rl):
            if self.routes:
                r1 = random.choice(self.routes)
                self.solution_routes.append(r1)
                self.routes.remove(r1)
            else:
                r1 = random.choice(self.solution_routes)
                self.solution_routes.append(r1)


    ## Transforms the solution routes into solution links of devices.
    #
    #@return has no return.
    def solution_Links(self, tsn):
        self.solution_links.clear()
        for route in self.solution_routes:
            for i in range(0, len(route) - 1):
                src_device = route[i]
                dest_device = route[i + 1]
                for link in tsn.links:
                    if (link.src == src_device) and (link.dest == dest_device):
                        self.solution_links.append(link)

    ##  Calculates the cost of a stream depending of the bandwidth used.
    #
    #   If the used link bandwidth surpasses the available bandwidth of a link then the cost of the link is given a heavy penalty by factor of 10
    #
    # @return stream cost, which is the sum of all link bandwidth that is used by the stream.
    def stream_cost(self, tsn):
        self.solution_Links(tsn)
        cost = 0
        for link in self.solution_links:
            link.used_bandwidth += self.stream_bandwidth
            cost += link.used_bandwidth
            if link.used_bandwidth > link.bandwidth:
                cost = cost * 10
        return cost

    #Chooses a random route from an array of all possible routes and exchanges it with a route from the solutions.
    #
    #@return Two random routes and is used to calculate the new solution cost in the simulating annealing.
    def random_exchange(self, random_stream):
        r1 = random.choice(self.routes)
        r2 = random.choice(self.solution_routes)

        random_stream.routes.remove(r1)
        random_stream.routes.append(r2)

        random_stream.solution_routes.remove(r2)
        random_stream.solution_routes.append(r1)
        return r1, r2

    def printRouteLinks(self, tsn):
        self.solution_links.clear()
        print("\n \33[31m", self.id, "\033[0m")
        k = 1
        for route in self.solution_routes:
            print("   \33[32m route ", k, "\33[0m")
            k += 1
            for i in range(0, len(route) - 1):
                src_device = route[i]
                dest_device = route[i + 1]
                for link in tsn.links:
                    if (link.src == src_device) and (link.dest == dest_device):
                        self.solution_links.append(link)
                        print("    link src=\033[96m", link.src.name, "\033[0m  dest=\033[92m", link.dest.name,
                              "\033[0m")
