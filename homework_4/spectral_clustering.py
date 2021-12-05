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


def read_edge_data(filepath: str) -> list:
    with open(filepath) as f:
        lines = f.readlines()
    edge_list = []
    for i, line in enumerate(lines):
        line_split = line.strip().split(',')
        u = int(line_split[0]) - 1
        v = int(line_split[1]) - 1
        edge_list.append((u, v))
    return edge_list


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
    adj_matrix = get_affinity_matrix(edge_list)
    print(adj_matrix)
    eigenvalues = np.linalg.eig(adj_matrix)
    print(eigenvalues)


if __name__ == '__main__':
    main()
