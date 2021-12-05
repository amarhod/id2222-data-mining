from __future__ import annotations
import argparse
from spectral_clustering import SpectralClustering


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', nargs='?', default='data/example1.dat', type=str)
    parser.add_argument('--k', nargs='?', default=2, type=int)
    return parser.parse_args()


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


def main():
    args = get_args()
    edge_list = read_edge_data(args.path)
    sc = SpectralClustering(edge_list, 3)
    print(sc.cluster_labels)


if __name__ == '__main__':
    main()
