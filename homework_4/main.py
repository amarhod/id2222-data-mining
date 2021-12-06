from __future__ import annotations
import argparse
import matplotlib.pyplot as plt
import networkx as nx
from spectral_clustering import SpectralClustering


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', nargs='?', default='data/example1.dat', type=str)
    parser.add_argument('--k', nargs='?', default=4, type=int)
    return parser.parse_args()


def plot_graph_clustering(graph, labels: list[int]):
    nx.draw(graph, node_size=30, node_color=labels)
    plt.show()


def plot_fiedler_vector(graph):
    if not nx.is_connected(graph):
        return
    fiedler_vector = sorted(nx.fiedler_vector(graph))
    plt.plot(fiedler_vector)
    plt.show()


def main():
    args = get_args()
    graph_data = nx.read_edgelist(args.path, delimiter=',', nodetype=int, data=(('weight', int),))
    graph = nx.Graph()
    graph.add_nodes_from(sorted(graph_data.nodes))
    graph.add_edges_from(graph_data.edges)
    sc = SpectralClustering(graph_data.edges, args.k)
    plot_graph_clustering(graph, sc.cluster_labels)
    plot_fiedler_vector(graph)


if __name__ == '__main__':
    main()
