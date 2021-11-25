from __future__ import annotations
import argparse
import timeit
from association_rules import Associator
from frequent_itemsets import FrequentItemsets


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', nargs='?', default='data/T10I4D100K.dat', type=str)
    parser.add_argument('--itemset_size', nargs='?', default=1_000_000, type=int)
    parser.add_argument('--number_of_baskets', nargs='?', default=100_000, type=int,
                        help='number of baskets used from the data set')
    parser.add_argument('--support', nargs='?', default=1000, type=int)
    parser.add_argument('--confidence', nargs='?', default=0.5, type=float)
    return parser.parse_args()


def read_basket_data(number_of_baskets: int, filepath='data/T10I4D100K.dat') -> list[list]:
    with open(filepath) as f:
        lines = f.readlines()
    baskets = []
    for i, line in enumerate(lines):
        if i >= number_of_baskets:
            break
        baskets.append(list(map(int, line.strip().split(' '))))
    return baskets


def main():
    args = get_args()
    baskets = read_basket_data(args.number_of_baskets, args.dataset_path)
    time_start_frequent = timeit.default_timer()
    frequent_itemssets = FrequentItemsets(baskets, args.itemset_size, args.support)
    time_end_frequent = timeit.default_timer()
    association = Associator(frequent_itemssets.itemsets, args.confidence)
    time_end_association = timeit.default_timer()
    print(f'There are {len(frequent_itemssets.itemsets)} itemsets with support at or above {args.support}:\n',
          frequent_itemssets.itemsets)
    print(f"Association rules with a confidence of at least {args.confidence}:\n{association.rules}")
    print(f'Time to find frequent items: {round(time_end_frequent-time_start_frequent, 2)}')
    print(f'Time to find association rules: {round(time_end_association-time_end_frequent, 2)}')


if __name__ == '__main__':
    main()
