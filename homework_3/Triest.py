"""
Implementation of the triest Base and improved algorithms. Paper can be found at
http://www.kdd.org/kdd2016/papers/files/rfp0465-de-stefaniA.pdf
"""
import random


class Triest():

    def __init__(self, stream, memory_size):
        self.stream = stream
        self.memory_size = memory_size
        self.sample_set = set()
        self.counters = {}
        self.t = 0
        self.tau = 0  # global counter for the estimation of number of global triangles
        self.current_global_estimation = 0
        self.current_counter_estimations = {}
        self.run()

    def get_estimations(self, t):
        denominator = (self.memory_size * (self.memory_size - 1) * (self.memory_size - 2))
        print(f"Estimations for {t=}, {self.memory_size=}, {denominator=}")
        val = (t*(t-1) * (t-2)) / denominator
        e = max(1, val)
        for k, val in self.counters.items():
            self.current_counter_estimations[k] = e * val
        print(f"{self.tau=}, {e=}")
        self.current_global_estimation = self.tau * e

    def flip_biased_coin(self, probability):
        return "H" if random.random() < probability else "T"

    def get_neibourhood(self, graph, vertex):
        """
        Given a graph, represented as a set of edges (u,v), returns the neighboors of a given vertex.
        A vertex u has a neighbour x, if there is an edge (u,x) or (x,u) in the graph
        """
        neighbourhood = set()
        for edge in graph:
            if edge[0] == vertex:
                neighbourhood.add(edge[1])
            if edge[1] == vertex:
                neighbourhood.add(edge[0])
        return neighbourhood

    def run(self):
        print(f"Length of stream {len(self.stream)}")
        for edge in self.stream:
            self.t += 1
            if self.sample_edge(edge, self.t):
                self.sample_set.add(edge)
                self.update_counters("+", edge)
        self.get_estimations(self.t)

    def sample_edge(self, edge, t):
        if t <= self.memory_size:
            return True
        elif self.flip_biased_coin(self.memory_size/t) == "H":
            edge_to_remove = random.sample(self.sample_set, 1)[0]
            self.sample_set.remove(edge_to_remove)
            self.update_counters("-", edge_to_remove)
            return True
        return False

    def update_counter(self, op, counter):
        if op == "+":
            self.counters[counter] = self.counters.get(counter, 0) + 1
        else:
            self.counters[counter] = self.counters.get(counter, 0) - 1
        if self.counters[counter] <= 0:
            del self.counters[counter]

    def update_counters(self, op, edge):
        u = edge[0]
        v = edge[1]
        n_u = self.get_neibourhood(self.sample_set, u)
        n_v = self.get_neibourhood(self.sample_set, v)
        intersection = set.intersection(n_u, n_v)  # FOR SOME FUCKIN REASON THE INTERSECTION IS ALWAYS AN EMPTY SET FOR THE DATASET
        print(f"{n_u=} {n_v=} {intersection=}")
        for c in intersection:
            if op == "+":
                self.tau += 1
            else:
                self.tau -= 1
            self.update_counter(op, c)
            self.update_counter(op, u)
            self.update_counter(op, v)


if __name__ == "__main__":
    edges = [(1, 2), (2, 3), (32, 3), (3, 4), (1, 2), (2, 3), (32, 3), (3, 4), (1, 2), (2, 3), (32, 3), (3, 4)]
    trist = Triest(edges, 6)
    print(trist.current_global_estimation)
    print(trist.current_counter_estimations)
