"""
Implementation of the triest Base and improved algorithms. Paper can be found at
http://www.kdd.org/kdd2016/papers/files/rfp0465-de-stefaniA.pdf
"""
import random


class TriestImproved():
    def __init__(self, stream, memory_size):
        self.stream = stream
        self.memory_size = memory_size
        self.sample_set = set()
        self.counters = {}
        self.t = 0
        self.tau = 0  # global counter for the estimation of number of global triangles
        self.run()

    def flip_biased_coin(self, probability):
        return 'H' if random.random() <= probability else 'T'

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

    def sample_edge(self, edge, t):
        if t <= self.memory_size:
            return True
        elif self.flip_biased_coin(self.memory_size / t) == 'H':
            edge_to_remove = random.sample(self.sample_set, 1)[0]
            self.sample_set.remove(edge_to_remove)
            return True
        return False

    def update_counters(self, edge):
        u = edge[0]
        v = edge[1]
        n_u = self.get_neibourhood(self.sample_set, u)
        n_v = self.get_neibourhood(self.sample_set, v)
        intersection = n_u.intersection(n_v)
        for c in intersection:
            eta = (self.t - 1) * (self.t - 2) / (self.memory_size * (self.memory_size - 1))
            weight = max(1, eta)
            self.tau += weight
            self.counters[c] = self.counters.get(c, 0) + weight
            self.counters[u] = self.counters.get(u, 0) + weight
            self.counters[v] = self.counters.get(v, 0) + weight

    def run(self):
        for edge in self.stream:
            self.t += 1
            self.update_counters(edge)
            if self.sample_edge(edge, self.t):
                self.sample_set.add(edge)

if __name__ == '__main__':
    edges = [(1, 2), (2, 3), (32, 3), (3, 4), (1, 2), (2, 3), (32, 3), (3, 4), (1, 2), (2, 3), (32, 3), (2, 4)]
    trist = TriestImproved(edges, 12)
    print(trist.tau)
    print(trist.counters)
