import itertools


class FrequentItemsets():
    def __init__(self, baskets: list[list], k: int, support: int) -> None:
        self.baskets, self.k, self.support = baskets, k, support
        self.itemsets = self.find_frequent_itemsets(k)

    def find_item_frequency(self) -> dict[str, int]:
        """Finds frequency for singleton itemsets (k=1)
        """
        item_frequency = {}
        for basket in self.baskets:
            for item in basket:
                item_count = item_frequency.get(str(item), 0)
                item_frequency[str(item)] = item_count + 1
        return item_frequency

    def find_frequent_itemsets(self, k: int) -> dict[str, int]:
        """Finds frequency for itemsets with size k
        """
        item_frequency = {}
        for i in range(1, k + 1):
            if i == 1:
                item_frequency = self.find_item_frequency()
                item_frequency = filter_items_with_support(item_frequency, self.support)  # Remove items without support
            else:
                unique_items = get_unique_items_from_itemsets(item_frequency)
                possible_itemsets = list(itertools.combinations(unique_items, i))
                for basket in self.baskets:
                    for possible_itemset in possible_itemsets:
                        if set(possible_itemset) <= set(basket):  # Check if possible_itemset is a subset of the basket
                            increment_frequency_for_itemset(item_frequency,
                                                            '-'.join(map(str, sorted(possible_itemset))))
                item_frequency = filter_items_with_support(item_frequency, self.support)
        return item_frequency


def increment_frequency_for_itemset(item_frequency: dict[str, int], item: list[int]) -> None:
    item_frequency[item] = item_frequency.get(item, 0) + 1


def filter_items_with_support(item_frequency: dict[str, int], support: int) -> dict[str, int]:
    return {k: v for (k, v) in item_frequency.items() if v >= support}


def get_unique_items_from_itemsets(item_frequency: dict[str, int]) -> list[int]:
    """Creates a list of unique items from the itemsets (which are represented as strings)
    """
    unique_items = set()
    for item_set in item_frequency.keys():
        for item in map(int, item_set.split('-')):
            unique_items.add(int(item))
    return list(unique_items)


if __name__ == '__main__':
    baskets = [[0, 4, 5],
               [1, 4],
               [2, 4, 5],
               [0, 5],
               [1, 2, 3, 4, 5]]
    frequent_itemsets = FrequentItemsets(baskets, 3, 2)
    print(frequent_itemsets.itemsets)
