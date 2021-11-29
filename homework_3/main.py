from __future__ import annotations
import argparse
from triest_base import Triest
from triest_improved import TriestImproved


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', nargs='?', default='./data/data.txt', type=str)
    parser.add_argument('--number_of_lines', nargs='?', default=88234, type=int)
    parser.add_argument('--memory_size', nargs='?', default=1000, type=int)
    parser.add_argument('--improved', action='store_true')
    return parser.parse_args()


def read_edge_data(number_of_edges: int, filepath) -> set:
    with open(filepath) as f:
        lines = f.readlines()
    edges = set()
    for i, line in enumerate(lines):
        if i >= number_of_edges:
            break
        line_split = line.strip().split(' ')
        u = int(line_split[0])
        v = int(line_split[1])
        edge = (u, v) if u < v else (v, u)
        edges.add(edge)
    return edges


def main():
    args = get_args()
    number_of_edges = args.number_of_lines
    print(f'Settings: Length of stream = {number_of_edges}, Memory size = {args.memory_size}')
    edges = read_edge_data(number_of_edges=number_of_edges, filepath=args.path)
    if args.improved:
        trist = TriestImproved(edges, args.memory_size)
    else:
        trist = Triest(edges, args.memory_size)
    print('Global estimation:', trist.current_global_estimation)


if __name__ == '__main__':
    main()
