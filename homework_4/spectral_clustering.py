"""
Implementation of the Spectral clustering algorithm. Paper can be found at
https://ai.stanford.edu/~ang/papers/nips01-spectral.pdf
"""
from __future__ import annotations
import math
import numpy as np
from sklearn.cluster import KMeans


class SpectralClustering():
    def __init__(self, edges: list, k: int, affinity=False) -> None:
        self.edges = np.array(edges)
        self.k = k
        if affinity:  # Decides if we use an adjacency or affinity matrix
            self.A = self.get_affinity_matrix()
        else:
            self.A = self.get_adjacency_matrix()
        self.D = np.diag(np.sum(self.A, axis=1))
        self.L = np.dot(np.dot(np.linalg.inv(np.sqrt(self.D)), self.A), np.linalg.inv(np.sqrt(self.D)))
        self.X = self.get_k_eigenvectors(self.L, self.k)
        self.Y = self.get_renormalized_matrix(self.X)
        self.cluster_labels = KMeans(n_clusters=k).fit(self.Y).labels_

    def get_affinity_matrix(self) -> np.ndarray:
        matrix = np.zeros((self.edges.max(), self.edges.max()))
        for u, v in self.edges:
            a = round(affinity(u-1, v-1), 2)
            matrix[u-1, v-1] = a
            matrix[v-1, u-1] = a
        return matrix

    def get_k_eigenvectors(self, m: np.ndarray, k: int) -> np.ndarray:
        _, eigenvectors = np.linalg.eigh(m)
        return eigenvectors[:, -k:]

    def get_renormalized_matrix(self, m: np.ndarray) -> np.ndarray:
        Y = np.zeros_like(m)
        for i, row in enumerate(m):
            divider = np.sqrt(np.dot(row, row.T))
            Y[i] = row / divider
        return Y

    def get_adjacency_matrix(self) -> np.ndarray:
        matrix = np.zeros((self.edges.max(), self.edges.max()))
        for u, v in self.edges:
            matrix[u-1, v-1] = 1
            matrix[v-1, u-1] = 1
        return matrix


def affinity(u, v, sig=1) -> float:
    if u == v:
        return 0.0
    a = math.pow(abs(u - v), 2)
    b = 2 * math.pow(sig, 2)
    return math.exp(- a / b)


def main():
    edge_list = [(1, 2), (1, 3), (2, 5), (3, 2), (3, 4), (4, 6), (5, 4)]
    SC = SpectralClustering(edge_list, 2)
    print(SC.cluster_labels)


if __name__ == '__main__':
    main()
