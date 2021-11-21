import argparse
import timeit
from frequent_itemsets import FrequentItemsets


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--itemset_size', nargs='?', default=1_000_000, type=int)
    parser.add_argument('--number_of_baskets', nargs='?', default=100_000, type=int,
                        help='number of baskets used from the data set')
    parser.add_argument('--support', nargs='?', default=1000, type=int)
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
    baskets = read_basket_data(args.number_of_baskets)
    frequent_itemssets = FrequentItemsets(baskets, args.itemset_size, args.support)
    print(f'There are {len(frequent_itemssets.itemsets)} itemsets with support at or above {args.support}:',
          frequent_itemssets.itemsets)


if __name__ == '__main__':
    time_start = timeit.default_timer()
    main()
    time_end = timeit.default_timer()
    print(f'Time to execute: {time_end-time_start}')
