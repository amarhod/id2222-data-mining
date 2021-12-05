"""
Implementation of the Spectral clustering algorithm. Paper can be found at
https://ai.stanford.edu/~ang/papers/nips01-spectral.pdf
"""
from __future__ import annotations
import math
import numpy as np
from sklearn.cluster import KMeans


class SpectralClustering():
    def __init__(self, edges: list, k: int) -> None:
        self.edges = np.array(edges)
        self.k = k
        self.A = self.get_affinity_matrix()
        self.D = np.diag(np.sum(self.A, axis=1))
        self.L = np.dot(np.dot(np.linalg.inv(np.sqrt(self.D)), self.A), np.linalg.inv(np.sqrt(self.D)))
        self.X = self.get_k_eigenvectors(self.L, self.k)
        self.Y = self.get_renormalized_matrix(self.X)
        self.cluster_labels = KMeans(n_clusters=k).fit(self.Y).labels_

    def get_affinity_matrix(self):
        matrix = np.zeros((self.edges.max() + 1, self.edges.max() + 1))
        for u, v in self.edges:
            a = round(affinity(u, v), 2)
            matrix[u, v] = a
            matrix[v, u] = a
        return matrix

    def get_k_eigenvectors(self, m, k):
        _, eigenvectors = np.linalg.eigh(m)
        return eigenvectors[:, -k:]

    def get_renormalized_matrix(self, m):
        Y = np.zeros_like(m)
        for i, row in enumerate(m):
            divider = np.sqrt(np.dot(row, row.T))
            Y[i] = row / divider
        return Y

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
    SC = SpectralClustering(edge_list, 2)
    print(SC.A)
    print(SC.D)
    print(SC.X)
    print(SC.Y)
    print(SC.cluster_labels)


if __name__ == '__main__':
    main()
