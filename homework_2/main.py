from frequent_itemsets import FrequentItemsets


def read_basket_data(filepath='data/T10I4D100K.dat') -> list[list]:
    with open(filepath) as f:
        lines = f.readlines()
    baskets = []
    for line in lines:
        baskets.append(list(map(int, line.strip().split(' '))))
    return baskets


def main():
    baskets = read_basket_data()
    frequent_itemssets = FrequentItemsets(baskets, 2, 10)
    print(frequent_itemssets.itemsets)


if __name__ == '__main__':
    main()
