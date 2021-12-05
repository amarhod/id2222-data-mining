"""
Implementation of the Spectral clustering algorithm. Paper can be found at
https://ai.stanford.edu/~ang/papers/nips01-spectral.pdf
"""
from __future__ import annotations
import math
import numpy as np


def affinity(u, v, sig=1):
    if u == v:
        return 0
    a = math.pow(abs(u - v), 2)
    b = 2 * math.pow(sig, 2)
    return math.exp(- a / b)


def get_adjacency_matrix(edges: list):
    edges = np.array(edges)
    matrix = np.zeros((edges.max() + 1, edges.max() + 1))
    matrix[edges[:, 0], edges[:, 1]] = 1
    matrix[edges[:, 1], edges[:, 0]] = 1
    return matrix


def get_affinity_matrix(edges: list):
    edges = np.array(edges)
    matrix = np.zeros((edges.max() + 1, edges.max() + 1))
    for u, v in edges:
        a = round(affinity(u, v), 2)
        matrix[u, v] = a
        matrix[v, u] = a
    return matrix


def get_diagonal_matrix(affinity_matrix):
    matrix = np.zeros(affinity_matrix.shape)
    for i in range(matrix.shape[0]):
        matrix[i, i] = affinity_matrix[i].sum()
    return matrix


def main():
    edge_list = [(0, 1), (0, 4), (1, 4), (2, 1), (2, 3), (3, 5), (4, 3)]
    A = get_affinity_matrix(edge_list)
    print(A)
    D = get_diagonal_matrix(A)
    print(D)
    eigenvalues = np.linalg.eig(A)
    print(eigenvalues)


if __name__ == '__main__':
    main()
