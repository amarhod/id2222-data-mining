"""
Implementation of the Spectral clustering algorithm. Paper can be found at
https://ai.stanford.edu/~ang/papers/nips01-spectral.pdf
"""
from __future__ import annotations
import math
import numpy as np


class SpectralClustering():
    def __init__(self, edges: list, k: int) -> None:
        self.edges = np.array(edges)
        self.k = k
        self.A = self.get_affinity_matrix()
        self.D = np.diag(np.sum(self.A, axis=1))
        self.eigenvalues = np.linalg.eig(self.A)

    def get_affinity_matrix(self):
        matrix = np.zeros((self.edges.max() + 1, self.edges.max() + 1))
        for u, v in self.edges:
            a = round(affinity(u, v), 2)
            matrix[u, v] = a
            matrix[v, u] = a
        return matrix

    def get_adjacency_matrix(self):
        matrix = np.zeros((self.edges.max() + 1, self.edges.max() + 1))
        matrix[self.edges[:, 0], self.edges[:, 1]] = 1
        matrix[self.edges[:, 1], self.edges[:, 0]] = 1
        return matrix


def affinity(u, v, sig=1):
    if u == v:
        return 0
    a = math.pow(abs(u - v), 2)
    b = 2 * math.pow(sig, 2)
    return math.exp(- a / b)


def main():
    edge_list = [(0, 1), (0, 4), (1, 4), (2, 1), (2, 3), (3, 5), (4, 3)]
    SC = SpectralClustering(edge_list, 0)
    print(SC.A)
    print(SC.D)
    print(SC.eigenvalues)


if __name__ == '__main__':
    main()
