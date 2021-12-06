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


def plot_graph_clustering(graph_data, labels: list[int]):
    nx.draw(nx.Graph(graph_data), node_size=30, node_color=labels)
    plt.show()


def main():
    args = get_args()
    graph_data = nx.read_edgelist(args.path, delimiter=',', nodetype=int)
    sc = SpectralClustering(graph_data.edges, args.k)
    plot_graph_clustering(graph_data, sc.cluster_labels)


if __name__ == '__main__':
    main()
