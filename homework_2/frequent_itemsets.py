import itertools


class FrequentItemsets():
    def __init__(self, baskets: list[list], k: int, support: int) -> None:
        self.baskets, self.k, self.support = baskets, k, support
        self.itemsets = self.find_frequent_itemsets(k)

    def find_frequent_items(self) -> dict[tuple, int]:
        """Find frequency for singleton itemsets (k=1)
        """
        item_frequency = {}
        for basket in self.baskets:
            for item in basket:
                item_count = item_frequency.get((item,), 0)
                item_frequency[(item,)] = item_count + 1
        return item_frequency

    def find_frequent_itemsets(self, k: int) -> dict[tuple, int]:
        """Find frequency for k-itemsets by going through each transaction and checking there is support
           for any of the possible k-itemsets.
           This is done by creating k-sized combinations of the transaction and checking if any of them
           are in our candidate k-itemsets. It is more efficiant than looping over all candidates and
           finding support in the transaction.
        """
        itemset_frequency = {}
        number_of_itemsets = 0
        for i in range(1, k + 1):
            if i == 1:
                itemset_frequency = self.find_frequent_items()
                itemset_frequency = filter_items_with_support(itemset_frequency, self.support)
                self.singletons = [item for item in itemset_frequency]
            else:
                possible_itemsets = self.get_candidate_itemsets(itemset_frequency)
                for basket in self.baskets:
                    basket_itemsets = list(itertools.combinations(basket, i))
                    for itemset in basket_itemsets:
                        itemset = tuple(sorted(itemset))
                        if itemset in possible_itemsets:  # Check if possible_itemset is a subset of the basket
                            increment_frequency_for_itemset(itemset_frequency, itemset)

                itemset_frequency = filter_items_with_support(itemset_frequency, self.support)

            if len(itemset_frequency) <= number_of_itemsets:  # Stop searching if no new itemsets found for current k
                break
            else:
                number_of_itemsets = len(itemset_frequency)
        return itemset_frequency

    def get_candidate_itemsets(self, itemset_frequency: dict[tuple, int]) -> set:
        """Generate k-itemsets with supported k-1-itemsets and singletons
        """
        itemset_candidates = set()
        for itemset in itemset_frequency:
            for singleton in self.singletons:
                if singleton not in itemset:
                    itemset_candidates.add(tuple(sorted(itemset + singleton)))
        return itemset_candidates


def increment_frequency_for_itemset(itemset_frequency: dict[tuple, int], item: tuple) -> None:
    itemset_frequency[item] = itemset_frequency.get(item, 0) + 1


def filter_items_with_support(itemset_frequency: dict[tuple, int], support: int) -> dict[tuple, int]:
    return {k: v for (k, v) in itemset_frequency.items() if v >= support}


if __name__ == '__main__':
    baskets = [[0, 4, 5],
               [1, 4],
               [2, 4, 5],
               [0, 5],
               [1, 2, 3, 4, 5]]
    frequent_itemsets = FrequentItemsets(baskets, 3, 2)
    print(frequent_itemsets.itemsets)
