from __future__ import annotations
import argparse
from Triest import Triest


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", nargs="?", default="./data/data.txt", type=str)
    parser.add_argument("--number_of_lines", nargs="?", default=88234, type=int)
    parser.add_argument("--memory_size", nargs="?", default=1000, type=int)
    return parser.parse_args()


def read_edge_data(number_of_edges: int, filepath) -> list[list]:
    with open(filepath) as f:
        lines = f.readlines()
    edges = set()
    for i, line in enumerate(lines):
        if i >= number_of_edges:
            break
        line_split = line.strip().split(" ")
        left = int(line_split[0])
        right = int(line_split[1])
        edge = (left, right)
        edges.add(edge)
    return edges


def main():
    args = get_args()
    number_of_edges = args.number_of_lines
    print(f"Settings: num of edges {number_of_edges}, path {args.path}, mem size {args.memory_size}")
    edges = read_edge_data(number_of_edges=number_of_edges, filepath=args.path)
    trist = Triest(edges, 100)
    print(trist.current_global_estimation)
    print(trist.current_counter_estimations)


if __name__ == "__main__":
    main()
