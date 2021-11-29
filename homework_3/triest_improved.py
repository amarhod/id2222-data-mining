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
        self.current_global_estimation = 0
        self.current_counter_estimations = {}
        self.run()

    def get_estimations(self, t):
        denominator = (self.memory_size * (self.memory_size - 1) * (self.memory_size - 2))
        val = (t * ((t - 1) * (t - 2))) / denominator
        eps = max(1, val)
        for k, val in self.counters.items():
            self.current_counter_estimations[k] = round(eps * val)
        print(f'{self.tau=}, {eps=}')
        self.current_global_estimation = round(self.tau * eps)

    def flip_biased_coin(self, probability):
        return 'H' if random.random() < probability else 'T'

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
        for edge in self.stream:
            self.t += 1
            self.update_counters(edge)
            if self.sample_edge(edge, self.t):
                self.sample_set.add(edge)
        self.get_estimations(self.t)

    def sample_edge(self, edge, t):
        if t <= self.memory_size:
            return True
        elif self.flip_biased_coin(self.memory_size / t) == 'H':
            edge_to_remove = random.sample(self.sample_set, 1)[0]
            self.sample_set.remove(edge_to_remove)
            return True
        return False

    def update_counter(self, counter):
        eta = ((self.t - 1) * (self.t - 2)) / (self.memory_size * (self.memory_size - 1))
        self.counters[counter] = self.counters.get(counter, 0) + max(1, eta)

    def update_counters(self, edge):
        u = edge[0]
        v = edge[1]
        n_u = self.get_neibourhood(self.sample_set, u)
        n_v = self.get_neibourhood(self.sample_set, v)
        intersection = n_u.intersection(n_v)
        for c in intersection:
            self.tau += 1
            self.update_counter(c)
            self.update_counter(u)
            self.update_counter(v)


if __name__ == '__main__':
    edges = [(1, 2), (2, 3), (32, 3), (3, 4), (1, 2), (2, 3), (32, 3), (3, 4), (1, 2), (2, 3), (32, 3), (2, 4)]
    trist = TriestImproved(edges, 12)
    print(trist.current_global_estimation)
    print(trist.current_counter_estimations)
